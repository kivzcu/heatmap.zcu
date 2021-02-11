/* global L */
/* global $ */

var mymap
var heatmapLayer = null
var markersLayer = null

// values for arrow keys
const arrowKeyLEFT = 37
const arrowKeyRIGHT = 39

var startX = 49.7248
var startY = 13.3521
var startZoom = 17

var dataSourceRoute
let positionsSourceRoute

let currentTime
let currentDate

var timer
var isAnimationRunning = false
var data = []

//
// info = {
//  DATASETNAME: {
//    items: Array,
//    number: Number,
//    datasetName: String
// }
// }
//
var info = []
let currentPageInPopup = 0

// dictionary for names of datasets
const datasetDictNameDisplayName = {}
var datasetSelected = []

// animate data only in one day
let lockedDay = false

// loading information for async operations
let loading = 0

// default loader showup delay
const defaultLoaderDelay = 1000

// map markers for all datasets
const dataMapMarkers = {}

const globalMarkersHolder = {}
// all marker from which popup was removed
// contains: {key:[L.circle,L.pupup]}
// key: x and y, x + '' + y string
let globalMarkersChanged = {}

const globalPopup = {
  coord: {
    lat: 0,
    lng: 0
  },
  _popup: null
}




const onDocumentReady = () => {
  $('#dropdown-dataset').on('click', function (e) {
    e.stopPropagation()
  })

  $('#btn-update-heatmap').prop('name', '')
  changeCurrentTime()
  changeCurrentDate()
  onValueChangeRegister()
  onArrowLeftRightKeysDownRegister()
}




/* ------------ DATA FETCHERS ------------ */

const genericFetch = async (route, method) => {
  const headers = new Headers()
  const request = new Request(route, {
    method: method,
    headers: headers
  })
  const beforeJson = await fetch(request)

  return beforeJson.json()
}

const fetchDatasetDataByDatetime = async (route, datasetName, date, time) => {
  return await genericFetch(route + '/' + datasetName + '/' + date + '/' + time, 'GET')
}

const fetchDatasetMapMarkers = async (route, datasetName) => {
  return await genericFetch(route + '/' + datasetName, 'GET')
}

preload = async (time, timeShift, date) => {
  loadingY()

  for (let nTime = time + timeShift; nTime >= 0 && nTime <= 23; nTime = nTime + timeShift) {
    if (!data[nTime]) {
      data[nTime] = {}
    }

    datasetSelected.forEach(async (datasetName) => {
      if (!data[nTime][datasetName]) {
        data[nTime][datasetName] = await fetchDatasetDataByDatetime(dataSourceRoute, datasetName, date, nTime)
      }
    })
  }

  loadingN()
}

/**
 * Load and display heatmap layer for current data
 * 
 * @param {string} opendataRoute route to dataset source
 * @param {string} positionsRoute  route to dataset positions source
 */
const loadCurrentTimeHeatmap = async (opendataRoute, positionsRoute, loaderDelay = defaultLoaderDelay) => {
  loadCheckboxDatasetNameData()

  dataSourceRoute = opendataRoute
  positionsSourceRoute = positionsRoute
  const allPromises = []
  data[currentTime] = {}

  const dataSelectedHandler = async (datasetName) => {
    if (!(datasetName in dataMapMarkers)) {
      dataMapMarkers[datasetName] = await fetchDatasetMapMarkers(positionsRoute, datasetName)
    }

    const datasetData = await fetchDatasetDataByDatetime(dataSourceRoute, datasetName, currentDateToString(), currentTime)
    data[currentTime][datasetName] = datasetData
  }

  datasetSelected.forEach((datasetName) => {
    allPromises.push(dataSelectedHandler(datasetName))
  })

  loadingY(loaderDelay)

  await Promise.all(allPromises).then(
    () => {
      loadingN(0)
      drawMapMarkers(dataMapMarkers)
      drawHeatmap(data[currentTime])

      preload(currentTime, 1, currentDateToString())
      preload(currentTime, -1, currentDateToString())
    }
  )
}

/**
 * Checks dataset availibility
 * @param {string} route authority for datasets availibility checks
 */
const checkDataSetsAvailability = async (route) => {
  const result = await genericFetch(route + '/' + currentDateToString(), 'POST')
  updateAvailableDataSets(result)
}




/* ------------ MAP ------------ */

/**
 * Initialize leaflet map on start position which can be default or set based on user action
 */
const initMap = () => {
  startX = localStorage.getItem('lat') || startX
  startY = localStorage.getItem('lng') || startY
  startZoom = localStorage.getItem('zoom') || startZoom

  mymap = L.map('heatmap').setView([startX, startY], startZoom)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '',
    maxZoom: 19
  }).addTo(mymap)

  mymap.on('click', function (e) { showPopup(e) })
}

const setMapView = (latitude, longitude, zoom) => {
  localStorage.setItem('lat', latitude)
  localStorage.setItem('lng', longitude)
  localStorage.setItem('zoom', zoom)

  mymap.setView([latitude, longitude], zoom)
}

const drawHeatmap = (dataRaw) => {
  const dataDict = dataRaw
  const mergedPoints = []
  let max = 0

  if (Object.keys(globalMarkersChanged).length) {
    Object.keys(globalMarkersChanged).forEach(function (key) {
      globalMarkersChanged[key][0].bindPopup(globalMarkersChanged[key][1])
    })
    globalMarkersChanged = {}
  }

  Object.keys(dataDict).forEach((key) => {
    const data = dataDict[key]
    max = Math.max(max, data.max)

    if (data != null) {
      // Bind back popups for markers (we dont know if there is any data for this marker or not)
      const points = data.items.map((point) => {
        const { x, y, number } = point
        const key = x + '' + y
        const holder = globalMarkersHolder[key]
        if (!globalMarkersChanged[key] && number) {
          // There is data for this marker => unbind popup with zero value
          holder[0] = holder[0].unbindPopup()
          globalMarkersChanged[key] = holder
        }

        return [x, y, number]
      })
      mergedPoints.push(...points)
    } else {
      if (heatmapLayer != null) {
        mymap.removeLayer(heatmapLayer)
      }
    }
  })

  if (heatmapLayer != null) {
    mymap.removeLayer(heatmapLayer)
  }

  if (mergedPoints.length) {
    heatmapLayer = L.heatLayer(mergedPoints, { max: max, minOpacity: 0.5, radius: 35, blur: 30 }).addTo(mymap)
  }

  updatePopup()
}

const drawMapMarkers = (data) => {
  if (markersLayer != null) {
    mymap.removeLayer(markersLayer)
  }

  markersLayer = L.layerGroup()

  Object.keys(data).forEach(key_ => {
    for (var key in data[key_]) {
      const { x, y, name } = data[key_][key]
      const pop =
        prepareLayerPopUp(x, y, 1, `popup-${key_}`)
          .setContent(getPopupContent(datasetDictNameDisplayName[key_], name, 0, 0, 1, 1))
      const newCircle =
        L.circle([x, y], { radius: 2, fillOpacity: 0.8, color: '#004fb3', fillColor: '#004fb3', bubblingMouseEvents: true })
          .bindPopup(pop)
      globalMarkersHolder[x + '' + y] = [newCircle, pop] // add new marker to global holders
      markersLayer.addLayer(
        newCircle
      )
    }
  })

  markersLayer.setZIndex(-1).addTo(mymap)
}




/* ------------ GUI ------------ */

const changeCurrentTime = (time = null) => {
  if (time !== null) {
    currentTime = time
  } else {
    currentTime = parseInt($('#dropdown-time input[type="radio"]:checked').val())
  }
}

const changeCurrentDate = (date = null) => {
  const dateInput = $('#date')
  currentDate = new Date(date ? date : dateInput.val())

  dateInput.val(currentDateToString())
  $('#player-date span').html(`${currentDate.getDate()}. ${currentDate.getMonth() + 1}. ${currentDate.getFullYear()}`)

  data = []
}

const toggleDayLock = () => {
  lockedDay = !lockedDay
  $('#player-date').toggleClass('lock')
}




/* ------------ POPUPS ------------ */

const setGlobalPopupContent = (content) => {
  globalPopup._popup.setContent(content)
  globalPopup._popup.openOn(mymap)
}

const getPaginationButtonsInPopup = (currentPage, countPages) => ({
  previousButton: '<button type="button" id="btn-popup-previous-page" onclick="js.setPreviousPageInPopup()"></button>',
  pagesList: `<p id="pages">${currentPage} z ${countPages}</p>`,
  nextButton: '<button type="button" id="btn-popup-next-page" class="next" onclick="js.setNextPageInPopup()"></button>'
})

const disablePopupPaginationButtons = () => {
  $('#btn-popup-previous-page').prop('disabled', true)
  $('#btn-popup-next-page').prop('disabled', true)
  $('.popup-pagination').hide()
}

const generatePopupPaginationButtons = (controls) => {
  return `<div class="popup-pagination">${controls ? controls.reduce((sum, item) => sum + item, '') : ''}</div>`
}

const getCountPagesInPopup = () => {
  const infoKeys = Object.keys(info)

  if (infoKeys.length === 1) {
    // return number of records in one dataset (one dataset in area)
    return info[infoKeys[0]].items.length
  }
  // return number of datasets (agregation of all datasets in area)
  return infoKeys.length
}

const getPopupDataOnPage = (pageInPopup) => {
  const keys = Object.keys(info)
  return info[keys[pageInPopup]]
}

const setPreviousPageInPopup = () => {
  const countPagesInPopup = getCountPagesInPopup()
  const page = currentPageInPopup

  currentPageInPopup = (currentPageInPopup + countPagesInPopup - 1) % countPagesInPopup
  setPageContentInPopup(page)
}

const setNextPageInPopup = () => {
  const countPagesInPopup = getCountPagesInPopup()
  const page = currentPageInPopup

  currentPageInPopup = (currentPageInPopup + 1) % countPagesInPopup
  setPageContentInPopup(page)
}

const genMultipleDatasetsPopUp = (sum, currentPage, countPages, datasetName) => {
  const popupHeader = `<strong id="dataset-name">${datasetName}</strong>`
  const popupData = `<div id="place-intesity"><span id="current-number">${sum}</span></div>`
  const { previousButton, nextButton, pagesList } = getPaginationButtonsInPopup(currentPage, countPages)

  return `
  ${popupHeader}
  ${popupData}
  ${generatePopupPaginationButtons([previousButton, pagesList, nextButton])}
  `
}

const prepareLayerPopUp = (lat, lng, num, className) => L.popup({
  autoPan: false,
  className: className
}).setLatLng([lat / num, lng / num])

const getPopupContent = (datasetName, placeName, currentCount, sum, currentPage, countPages) => {
  const popupHeader = `
    <strong>${datasetName}</strong>
    <div id="place-name">${placeName}</div>`
  const popupData = `
    <div id="place-intesity">
      <span id="current-number">${currentCount}</span>
      <span id="sum-number">${(sum && sum !== Number(currentCount)) ? '/' + sum : ''}</span>
    </div>`
  const { previousButton, nextButton, pagesList } = getPaginationButtonsInPopup(currentPage, countPages)

  return `
  ${popupHeader}
  ${popupData}
  ${generatePopupPaginationButtons(countPages > 1 ? [previousButton, pagesList, nextButton] : null)}
  `
}

const areMultipleDatasetsInRadius = () => {
  return Object.keys(info).length > 1
}

const setPopupDatasetClassName = (datasetName) => {
  const popup = $('.leaflet-popup')

  popup.removeClass(function (index, css) {
    return (css.match(/(^|\s)popup-\S+/g) || []).join(' ');
  })
  popup.addClass('popup-' + datasetName)
}

const showPopup = (e) => {
  info = []
  currentPageInPopup = 0

  const stile = 40075016.686 * Math.cos(startX) / Math.pow(2, mymap.getZoom())
  const radius = 25 * stile / 256

  let i = 0
  let lat = 0
  let lng = 0

  let total = 0

  const datasetsInRadius = {}
  const eventCoord = {
    lng: e.latlng.lng,
    lat: e.latlng.lat
  }

  Object.keys(data[currentTime]).forEach(key => {
    const namedData = data[currentTime][key]

    namedData.items.forEach(element => {
      if (e.latlng.distanceTo(new L.LatLng(element.x, element.y)) < radius) {
        lat += element.x
        lng += element.y
        info[i] = { place: element.place, number: element.number, datasetName: key }
        total += parseInt(element.number)
        i++
        datasetsInRadius[key] = true
      }
    })
  })

  // Process info for more then one dataset
  info = info.reduce((acc, item) => {
    if (!acc[item.datasetName]) {
      acc[item.datasetName] = {
        items: [],
        number: 0,
        datasetName: item.datasetName
      }
    }

    acc[item.datasetName].items.push(item)
    acc[item.datasetName].number += Number(item.number)
    return acc
  }, {})

  const countDatasets = Object.keys(datasetsInRadius).length

  if (!countDatasets) {
    if (mymap._popup) {
      $('#sum-number').text('')
      $('#current-number').html(0)
      disablePopupPaginationButtons()
    }

    return
  }

  if (countDatasets === 1) {
    const markersInRadius = getPopupDataOnPage(0)
    const popupPagesData = markersInRadius.items
    const { place, number } = popupPagesData[currentPageInPopup]

    if (!globalPopup._popup || !areCoordsIdentical(globalPopup.coord, eventCoord)) {
      globalPopup._popup = prepareLayerPopUp(lat, lng, i, `popup-${markersInRadius.datasetName}`)
      globalPopup.coord = eventCoord
    }
    else {
      setPopupDatasetClassName(markersInRadius.datasetName)
    }

    setGlobalPopupContent(getPopupContent(datasetDictNameDisplayName[markersInRadius.datasetName], place, number, total, 1, popupPagesData.length))

    if (popupPagesData.length === 1) {
      disablePopupPaginationButtons()
    }
  } else {
    const { datasetName, number } = getPopupDataOnPage(currentPageInPopup)

    if (!globalPopup._popup || !areCoordsIdentical(globalPopup.coord, eventCoord)) {
      globalPopup._popup = prepareLayerPopUp(lat, lng, i, `popup-${datasetName}`)
      globalPopup.coord = eventCoord
    }
    else {
      setPopupDatasetClassName(datasetName)
    }

    setGlobalPopupContent(genMultipleDatasetsPopUp(number, 1, getCountPagesInPopup(), datasetDictNameDisplayName[datasetName]))
  }
}

const setPageContentInPopup = (page) => {
  const previousPageData = areMultipleDatasetsInRadius() ? getPopupDataOnPage(page) : getPopupDataOnPage(0).items[page]
  const currentPageData = areMultipleDatasetsInRadius() ? getPopupDataOnPage(currentPageInPopup) : getPopupDataOnPage(0).items[currentPageInPopup]
  const datasetName = $('#dataset-name')

  if (datasetName) {
    datasetName.html(datasetDictNameDisplayName[currentPageData.datasetName])
  }

  $('#place-name').html(currentPageData.place ? currentPageData.place : currentPageData.datasetName)
  $('#current-number').html(currentPageData.number)
  $('#pages').html(currentPageInPopup + 1 + ' z ' + getCountPagesInPopup())

  $('.leaflet-popup').removeClass(`popup-${previousPageData.datasetName}`).addClass(`popup-${currentPageData.datasetName}`)
}

const updatePopup = () => {
  const { _popup } = mymap

  if (_popup) {
    showPopup({
      latlng: _popup.getLatLng()
    })
  }
}




/* ------------ ANIMATION ------------ */

/**
 * Change animation start from playing to stopped or the other way round
 */
const changeAnimationState = () => {
  const btnAnimate = $('#animate-btn')

  isAnimationRunning = !isAnimationRunning

  if (isAnimationRunning) {
    btnAnimate.removeClass('play').addClass('pause')
    timer = setInterval(function () { next() }, 800)
  } else {
    clearTimeout(timer)
    btnAnimate.removeClass('pause').addClass('play')
  }
}

const previous = async () => {
  if (loading) {
    return
  }

  currentTime = (currentTime + 23) % 24
  changeHour(currentTime)

  if (!lockedDay && currentTime === 23) {
    addDayToCurrentDate(-1)
    await loadCurrentTimeHeatmap(dataSourceRoute, positionsSourceRoute)
  } else {
    drawHeatmap(data[currentTime])
  }

  updatePopup()
}

const next = async () => {
  if (loading) {
    return
  }

  currentTime = (currentTime + 1) % 24
  changeHour(currentTime)

  if (!lockedDay && currentTime === 0) {
    addDayToCurrentDate(1)
    await loadCurrentTimeHeatmap(dataSourceRoute, positionsSourceRoute)
  } else {
    drawHeatmap(data[currentTime])
  }

  updatePopup()
}

const onChangeHour = (hour) => {
  changeHour(hour)
  drawHeatmap(data[currentTime])
}

const changeHour = (hour) => {
  $('#player-time').removeAttr('style')
  changeCurrentTime(hour)
  updateHeaderControls()
  setTimeline()
  changeUrlParameters()
  updatePopup()
}

const dragTimeline = () => {
  const hourElemWidthPx = 26

  const elem = $('#player-time')
  const offset = elem.offset().left - elem.parent().offset().left

  if (offset >= 0 && offset <= elem.parent().width()) {
    const hour = Math.round(offset / hourElemWidthPx)

    if (hour !== currentTime) {
      elem.attr('class', 'time hour-' + hour)
      $('#player-time span').html(formatTime(hour))

      onChangeHour(hour)
    }
  }
}

const onArrowLeftRightKeysDownRegister = () => {
  $(document).keydown(function (e) {
    const { which } = e

    if (which === arrowKeyLEFT) {
      previous()
      e.preventDefault()
    } else if (which === arrowKeyRIGHT) {
      next()
      e.preventDefault()
    }
  })
}

/**
 * Change browser url based on animation step.
 */
const changeUrlParameters = () => {
  window.history.pushState(
    '',
    document.title,
    window.location.origin + window.location.pathname + `?date=${currentDateToString()}&time=${currentTime}${datasetSelected.reduce((acc, current) => acc + '&type[]=' + current, '')}`
  )
}




/* ------------ UTILS ------------ */

const formatTime = (hours, twoDigitsHours = false) => {
  return ((twoDigitsHours && hours < 10) ? '0' : '') + hours + ':00';
}

const formatDate = (date) => {
  var day = String(date.getDate())
  var month = String(date.getMonth() + 1)

  if (day.length === 1) {
    day = '0' + day
  }

  if (month.length === 1) {
    month = '0' + month
  }

  // return YYYY-MM-DD
  return date.getFullYear() + '-' + month + '-' + day
}

const currentDayToString = () => {
  const day = currentDate.getDate()
  return day > 9 ? `${day}` : `0${day}`
}

const currentMonthToString = () => {
  const month = currentDate.getMonth() + 1
  return month > 9 ? `${month}` : `0${month}`
}

const currentDateToString = () => `${currentDate.getFullYear()}-${currentMonthToString()}-${currentDayToString()}`

const addDayToCurrentDate = (day) => {
  currentDate.setDate(currentDate.getDate() + day)
  changeCurrentDate(currentDate)
}

const areCoordsIdentical = (first, second) => {
  return first.lat === second.lat && first.lng === second.lng
}

const debounce = (func, delay) => {
  let inDebounce
  return function () {
    const context = this
    const args = arguments
    clearTimeout(inDebounce)
    inDebounce = setTimeout(() => func.apply(context, args), delay)
  }
}




/* ------------ GUI ------------ */

const updateHeaderControls = () => {
  $(`#time_${currentTime}`).prop('checked', true)
  $('#dropdownMenuButtonTime').html(formatTime(currentTime, true))
}

const initDatepicker = async (availableDatesSource) => {
  const result = await genericFetch(availableDatesSource, 'GET')
  const datesContainData = String(result).split(',')

  $('#date').datepicker({
    format: 'yyyy-mm-dd',
    language: 'cs',
    beforeShowDay: function (date) {
      if (datesContainData.indexOf(formatDate(date)) < 0) {
        return { enabled: false, tooltip: 'Žádná data' }
      } else {
        return { enabled: true }
      }
    },
    autoclose: true
  })
}

const initLocationsMenu = () => {
  const elmLocationsList = $('.locations')
  const locationsDisplayClass = 'show'

  if ($(window).width() <= 480) {
    elmLocationsList.removeClass(locationsDisplayClass)
  } else {
    elmLocationsList.addClass(locationsDisplayClass)
  }
}

const setTimeline = () => {
  $('#player-time > span').text(formatTime(currentTime))
  $('#player-time').attr('class', 'time hour-' + currentTime)
}

const onValueChangeRegister = () => {
  $('#date').change(function () {
    changeCurrentDate($(this).val())
    loadCurrentTimeHeatmap(dataSourceRoute, positionsSourceRoute, 0)
    changeUrlParameters()
  })

  $('#dropdown-time input[type="radio"]').each(function () {
    $(this).change(function () {
      changeHour(parseInt($(this).val()))
      drawHeatmap(data[currentTime])
    })
  })

  $('#dropdown-dataset input[type="checkbox"]').each(function () {
    $(this).change(
      debounce(() => onCheckboxClicked(this), 1000)
    )
  })
}

const onCheckboxClicked = async (checkbox) => {
  if ($(checkbox).prop('checked')) {
    await loadCurrentTimeHeatmap(dataSourceRoute, positionsSourceRoute, 0)
  } else {
    loadCheckboxDatasetNameData()

    data.forEach((item, index) => {
      Object.keys(item).forEach(datasetName => {
        if (datasetName === $(checkbox).val()) {
          delete data[index][datasetName]
        }
      })

      drawHeatmap(data[currentTime])
    })
  }

  updatePopup()
  changeUrlParameters()
}

const loadCheckboxDatasetNameData = () => {
  datasetSelected = []

  $('#dropdown-dataset .dropdown-item').each(function () {
    const input = $(this).find('input')
    const inputVal = input[0].value

    if (input[0].checked) {
      datasetSelected.push(inputVal)
    }

    datasetDictNameDisplayName[inputVal] = $(input).data('dataset-display-name')
  })
}

const updateAvailableDataSets = async (available) => {
  let leastOneOptionEnabled = false

  $('#dropdown-dataset .dropdown-item').each(function () {
    const input = $(this).find('input')

    if (!(input[0].value in available)) {
      $(this).addClass('disabled')
      $(input).prop('checked', false)
    } else {
      leastOneOptionEnabled = true
      $(this).removeClass('disabled')
    }
  })

  $('#btn-update-heatmap').prop('disabled', !leastOneOptionEnabled)
}




/* ------------ GUI LOADING ------------ */

const loadingCallbackNested = (func, delay) => {
  setTimeout(() => {
    func(loading)
    if (loading) {
      loadingCallbackNested(func, delay)
    }
  }, delay)
}

const loadingY = (delay = defaultLoaderDelay) => {
  loading++
  // check after nms if there is something that is loading
  loadingCallbackNested(() => loadingCallbackNested((isLoading) => loadingTimeline(isLoading), delay))
}

const loadingN = (delay = defaultLoaderDelay) => {
  loading--
  loadingCallbackNested(() => loadingCallbackNested((isLoading) => loadingTimeline(isLoading)), delay)
}

const loadingTimeline = (isLoading) => {
  if (isLoading) {
    loadingYTimeline()
  } else {
    loadingNTimeline()
  }
}

const loadingYTimeline = () => {
  $('#player-time > .spinner-border').removeClass('d-none')
  $('#player-time > span').text('')
}

const loadingNTimeline = () => {
  $('#player-time > .spinner-border').addClass('d-none')
  setTimeline()
}

module.exports = {
  initDatepicker,
  initLocationsMenu,
  initMap,
  onDocumentReady,
  checkDataSetsAvailability,
  loadCurrentTimeHeatmap,
  dragTimeline,
  setPreviousPageInPopup,
  setNextPageInPopup,
  previous,
  next,
  toggleDayLock,
  changeAnimationState,
  onChangeHour,
  setMapView
}