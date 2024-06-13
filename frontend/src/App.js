import './App.css';

import { useState, useEffect } from "react";
import axios from "axios";


function App() {
  const [travel, setTravel] = useState("")
  const [image, setImage] = useState("")


  const fetchAPITravel = async() => {
    const response = await axios.get("http://localhost:5000/travel");
    console.log(response)
    const data = response.data
    const travel = data[0]
    const image = data[1]
    setTravel(travel)
    setImage(image)
  }

  useEffect(() => {
    fetchAPITravel()
  }, [])

  return (
    <div className="App">
      <header className="App-header">
          {travel}
          <img src={image} width="500px"/>
      </header>
    </div>
  );
}

export default App;
