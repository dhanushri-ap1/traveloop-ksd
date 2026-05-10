document.getElementById("locationBtn").addEventListener("click", () => {
    window.geoLocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        console.log(`Location: ${lat}, ${lon}`);
        sendMessage(`My current location is Latitude: ${lat}, Longitude: ${lon}`);
      },
      (err) => {
        alert(`Failed to get location. Error: ${err.message}`);
      }
    );
  });
  
