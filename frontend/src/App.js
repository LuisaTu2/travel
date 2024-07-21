import "./App.css";

import { useState, useEffect } from "react";

import Photo from "./components/photo/Photo.js";
import { GET_PHOTOS_BEOGRAD, ARCHITECTURE_PATH } from "./constants.js";

function App() {
  const [photos, setPhotos] = useState([]);
  const [ipAddress, setIpAddress] = useState("");

  const getPhotos = async () => {
    const response = await fetch(GET_PHOTOS_BEOGRAD); 
    const data = await response.json();
    const photos = data.photos;
    setPhotos(photos);
  };

  const getIpAddress = async () => {
    const response = await fetch("https://api.ipify.org/?format=json");
    const data = await response.json();
    setIpAddress(data["ip"])
  }

  useEffect(() => {
    getPhotos();
    getIpAddress();
  }, []);

  return (
    <div className="app">
      <h1>beograd</h1>
      {ipAddress ? photos.map((photo) => {
        return <Photo data={photo} key={photo.title} ipAddress={ipAddress}/>;
      }) : []}
      <footer>
        <div>Curious about the implementation details? 
        Check out the <strong><a href={ARCHITECTURE_PATH} className="linkArchitecture" target="_blank"> architecture</a></strong> page!</div> 
        <p className="made"> made with <span>&#129293; </span> in <span>&#127809; </span></p>
      </footer>
    </div>
  );
}

export default App;
