import "./App.css";

import { useState, useEffect } from "react";

import Photo from "./Photo.js";
import { GET_PHOTOS_BEOGRAD } from "./constants.js";

function App() {
  const [photos, setPhotos] = useState([]);
  const [phrase, setPhrase] = useState();

  const getPhotos = async () => {
    const response = await fetch(GET_PHOTOS_BEOGRAD); 
    const data = await response.json();
    const photos = data.photos;
    setPhotos(photos);
  };

  useEffect(() => {
    getPhotos();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <ul>
          {photos.map((photo) => {
            return <Photo data={photo} key={photo.title} />;
          })}
          <div> with love {phrase} </div>
        </ul>
      </header>
    </div>
  );
}

export default App;
