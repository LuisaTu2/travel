import "./Photo.css";

export default function Photo({ data }) {
  const item = (
    <div className="photo">
      <img src={data.link} />
      <div className="photoMeta">
        <p className="photoTitle">{data.title}</p>
        <p className="photoDesc">{data.description} </p>

        <p className="photoReactions" onClick={event => { console.log("EVENT: ", event); event.target.style.color = "grey"}}>
          &#x2764; 
          {/* {data.reactions.like}{" "}  */}
          &#183;  
          &#128049; 
          {/* {data.reactions.macka}{" "}  */}
          &#183; 
          &#128054;
           {/* {data.reactions.doggo} */}
          {/* &#127788; 0 */}
        </p>
      </div>
    </div>
  );
  return item;
}