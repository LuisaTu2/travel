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
      <div className="memories">
        <h3> memories </h3>
        <ul>
          <li className="memory"> long nights and splav music quickly slip into foggy mornings and tired red yugos honk impatiently at heavily caffeinated souls</li>
          <li className="memory"> i can't stand turbo folk music. give me a bijelo dugme or zdravko čolić any day </li>
          <li className="memory"> beograd seems to be forever holding a secret</li>
          <li className="memory"> tebi bih dao i sredinu palacinke! </li>
          <li className="memory"> i am left to believe that the only way she will ever accept me is if I let her be. she is still finding her way and, eventually, she will figure herself out. 
          but be warned. her constant push and pull, her evasive looks and her rivers of rakija might be just enough to lure you in and make you want to never let go. </li>
          <li className="memory"> running every morning by the river. cevapi. walking kalemegdan with ana. walks and dinners with friends. 
          run for the cure with the girls. swimming at ada. silosi with the ladies. tango and latin nights. 
          coffee breaks at kafeteria. falling in love at šlep. gelato. oh, did I mention cevapi? </li>
          <li className="memory"> etched forever in mah heart is singing lipe cvatu on a boat with y'all. </li>
        </ul>
      </div>
      <footer>
        <div className="curious">Curious about the implementation details? 
        Check out the <strong><a href={ARCHITECTURE_PATH} className="linkArchitecture" target="_blank"> architecture</a></strong> page!</div> 
        <p className="made"> made with <span>&#129293; </span> in <span>&#127809; </span></p>
      </footer>
    </div>
  );
}

export default App;
