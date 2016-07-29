Storage.prototype.setObj = function (key, obj) {
    return this.setItem(key, JSON.stringify(obj))
};
Storage.prototype.getObj = function (key) {
    return JSON.parse(this.getItem(key))
};

function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) || [, null])[1]
    );
}


$(function () {
    var geocoder = new google.maps.Geocoder();

    navigator.geolocation.getCurrentPosition(function (pos) {
        var latLng = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
        geocoder.geocode({latLng: latLng}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK && results[0]) {
                $("#primary_location_name").val(results[0].formatted_address);
            }
//            if (status == google.maps.GeocoderStatus.OK && results[3]) {
//                $("#locality").val(results[3].formatted_address);
//            }
        });

        $("#latitude").val(pos.coords.latitude.toFixed(5));
        $("#longitude").val(pos.coords.longitude.toFixed(5));
        $("#elevation").val(pos.coords.altitude || 0);
    });
});

