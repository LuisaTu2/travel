import "./App.css";

import { useState, useEffect } from "react";
import axios from "axios";

import Photo from "./Photo.js";

function App() {
  const [photos, setPhotos] = useState([]);


  const getPhotos = async () => {
    const response = await axios.get("http://localhost:5000/get-photos", {
      params: { pattern: "beograd" },
    });
    const photos = response.data.photos;
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
        </ul>
      </header>
    </div>
  );
}

export default App;
