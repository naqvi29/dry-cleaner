var options = {
  values: "a, b, c",
  ajax: {
    url: "https://api.getaddress.io/find/SN3 1LG?api-key=WzJmU7wYw0aUaWMrieLDdA25832&format=true&sort=true&expand=true",
    type: "GET",
    dataType: "json",
    // Use "{{{q}}}" as a placeholder and Ajax Bootstrap Select will
    // automatically replace it with the value of the search query.
    data: {
      // q: "{{{q}}}"
    },
    beforeSend : function(xhr, opts){
        var query = $(".bs-searchbox input").val();
        if(query.length < 7){
            xhr.abort();
        }
        if(!isWithinRange(query)){
            response([{value:"We dont provide service in "+query.toUpperCase()}]);
            return;
        }
    },
  },
  locale: {
    emptyTitle: "Enter postcode"
  },
  log: 3,
  preprocessData: function(data) {
    var val = $(".bs-searchbox input").val();
    var i,
      l = data.addresses.length,
      array = [];
    if (l) {
      for (i = 0; i < l; i++) {
        var addressArray = data.addresses[i].filter(function (el) {
          return el != "";
        });
        var addressString = addressArray.join(", ")
        var optionValue = addressString;
        var json = {
          value : addressString + ", " + val.toUpperCase(),
        }
        array.push(json);
      }
    }
    // You must always return a valid array when processing data. The
    // data argument passed is a clone and cannot be modified directly.
    console.log(array);
    return array;
  }
};

$(".selectpicker")
  .selectpicker()
  .filter(".with-ajax")
  .ajaxSelectPicker(options);
$("select").trigger("change");

function chooseSelectpicker(index, selectpicker) {
  $(selectpicker).val(index);
  $(selectpicker).selectpicker('refresh');
}
