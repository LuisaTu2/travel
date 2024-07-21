import "./Photo.css";

import Reaction from "../reaction/Reaction.js";


export default function Photo({ data, ipAddress }) {
  const title = data.title;
  const description = data.description;
  const reactions = data.reactions;
  const l = Object.keys(reactions).length;
  const item = (
    <div className="photo">
      <img src={data.link} />
      <div className="photoMeta">
        <p className="photoTitle">{title}</p>
        {description ? <p className="photoDesc">{description} </p> : ""}
        { l > 0 ? <div className="photoReactions"> 
          {
            Object.entries(reactions).map((reaction, index) => {
              return <Reaction reaction={reaction} key={"r_" + index + title } isLast={index === (l - 1)} ipAddress={ipAddress} pk={data.pk} sk={data.sk}/>;
            })
          }
        </div> : ""
}
      </div>
    </div>
  );
  return item;
}
