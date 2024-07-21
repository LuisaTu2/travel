import "./Reaction.css";

export default function Reaction({reaction, isLast}) {
  const mapping = {
    "doggo" :  "🐶",
    "sun" : "☀️",
    "heart": "❤",
    "blue_heart": "💙",
    "black_heart": "🖤",
    "flower": "🌺",
    "coffee": "☕",
    "eyes": "👀",
  }
  const emoji = mapping[reaction[0]];
  const likes = reaction[1].likes;
  const r = (
    <div className="reaction">
        <p className="emoji"> {emoji}  </p>
        <p className="likes">  {likes} </p>
        {isLast ? "" : <p className="dot"> &#183; </p>}
    </div>
  );

    {/* <p className="photoReactions" onClick={event => { console.log("EVENT: ", event); event.target.style.color = "grey"}}>
</p> */}
  return r;
}
