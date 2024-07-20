import "./App.css";

import { useState, useEffect } from "react";

import Photo from "./Photo.js";
import { GET_PHOTOS_BEOGRAD, ARCHITECTURE_PATH } from "./constants.js";

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
          <div>Curious about the implementation details? </div> Check out the <strong><a href={ARCHITECTURE_PATH} style={{color: "white", textDecoration: "none"}}> architecture</a></strong> page.
          <footer>made with &#129293; in &#127809; </footer>
        </ul>
      </header>
    </div>
  );
}

export default App;
