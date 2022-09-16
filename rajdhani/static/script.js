const autocompleteURL = "/api/stations";
const searchURL = "/api/search";

function getQuerystring(obj) {
  return Object.entries(obj)
    .map((kv) => kv.map(encodeURIComponent))
    .map(([k, v]) => `${k}=${v}`)
    .join("&");
}

async function getAutocomplete(input) {
  const qs = getQuerystring({ q: input });
  const url = `${autocompleteURL}?${qs}`;

  const response = await fetch(url);
  const stations = await response.json();

  return stations.map(({ code, name }) => {
    return {
      value: code,
      text: `${name} - ${code}`,
    };
  });
}

async function searchTrains(from, to, date, ticketClass) {
  const qs = getQuerystring({ from,  to, date, ticket_class: ticketClass })
  const url = `${searchURL}?${qs}`

  const response = await fetch(url)
  const trains = await response.json()

  return trains
}

function selectFromStation(value, text) {
  $("#from-station-text").val(text);
  $("#from-station").val(value);
}

function selectToStation(value, text) {
  $("#to-station-text").val(text);
  $("#to-station").val(value);
}

function refreshAutocomplete(input, $list) {
  getAutocomplete(input)
    .then((stations) => {
      let html = stations
        .map(({ value, text }) => getAutocompleteItem(value, text))
        .join("\n");

      $list.html(
        stations
          .map(({ value, text }) => getAutocompleteItem(value, text))
          .join("\n")
      );
    })
    .catch((error) => {
      console.error(error);
    });
}

function getAutocompleteItem(value, text) {
  return `
        <li class="autocomplete-item" data-value="${value}">
            ${text}
        </li>`;
}

function getTrainCard(train) {
  return `
  <div class="card mb-2">
    <div class="card-header">
      <h5>${train.name} (${train.number})</h5>
    </div>
    <div class="card-body d-flex justify-content-between">
      <div>
        <h3>${train.departure}</h3>
        <h5>${train.from_station_name}</h5>
      </div>
      <div>
        <h3>${train.arrival}</h3>
        <h5>${train.to_station_name}</h5>
      </div>
    </div>
  </div>
  `
}

$(document).ready(function () {
  const $fromStationDiv = $("#from-station-div");
  const $toStationDiv = $("#to-station-div");
  const $fromList = $("#from-station-autocomplete-items");
  const $toList = $("#to-station-autocomplete-items");
  const $fromText = $("#from-station-text");
  const $toText = $("#to-station-text");

  $fromText.keyup(function () {
    const input = $(this).val();
    refreshAutocomplete(input, $fromList);
  });

  $toText.keyup(function () {
    const input = $(this).val();
    refreshAutocomplete(input, $toList);
  });

  $fromText.focusin(function () {
    $fromList.show();
  });

  $fromStationDiv.focusout(function (e) {
    $fromList.hide();
  });

  $toText.focusin(function () {
    $toList.show();
  });

  $toStationDiv.focusout(function () {
    $toList.hide();
  });

  $(".autocomplete-list").on("mousedown", ".autocomplete-item", function () {
    let text = $(this).text().trim();
    let { value } = $(this).data();
    value = value.trim()

    const $list = $(this).parent();
    let { valueTarget, textTarget } = $list.data();

    $(valueTarget).val(value);
    $(textTarget).val(text);
  });

  $("#trains-search").submit(async function(e) {
    e.preventDefault()

    let argsList = $(this).serializeArray()
    console.log("argslist", argsList)

    let args = argsList.reduce((a, {name, value}) => ({ ...a, [name]: value }), {})
    console.log("args", args)

    const trains = await searchTrains(args.from, args.to, args.date || "", args.ticket_class || "")
    console.log("trains", trains)

    $("#trains").html(
      trains.map(getTrainCard).join("\n")
    )

    $("#trains-container").show()
  })
});
