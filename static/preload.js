const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("geoLocation", {
  getCurrentPosition: (success, error) => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(success, error);
    } else {
      error({ message: "Geolocation not supported" });
    }
  },
});
