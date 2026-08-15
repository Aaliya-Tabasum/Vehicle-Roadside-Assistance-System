function useCurrentLocation() {

    const msg = document.getElementById("locMsg");

    if (!navigator.geolocation) {
        msg.innerHTML = "Geolocation is not supported.";
        msg.style.color = "red";
        return;
    }

    msg.innerHTML = "Fetching location...";

    navigator.geolocation.getCurrentPosition(

        function(position){

            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById("latitude").value = lat;
            document.getElementById("longitude").value = lon;

            // Reverse Geocoding
            fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`
            )
            .then(res => res.json())
            .then(data => {

                document.getElementById("location").value =
                    data.display_name;

                msg.innerHTML = "Current location detected.";
                msg.style.color = "#4ade80";

            })
            .catch(() => {

                document.getElementById("location").value =
                    lat + "," + lon;

                msg.innerHTML =
                    "Coordinates detected.";

                msg.style.color = "#4ade80";

            });

        },

        function(error){

            msg.style.color="red";

            switch(error.code){

                case error.PERMISSION_DENIED:
                    msg.innerHTML="Location permission denied.";
                    break;

                case error.POSITION_UNAVAILABLE:
                    msg.innerHTML="Location unavailable.";
                    break;

                case error.TIMEOUT:
                    msg.innerHTML="Location request timed out.";
                    break;

                default:
                    msg.innerHTML="Unable to fetch location.";
            }

        }

    );

}