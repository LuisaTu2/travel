import "./Photo.css";

export default function Photo({ data }) {
  const item = (
    <div className="photo">
      <img src={data.link} />
      <div className="photoMeta">
        <p className="photoTitle">{data.title}</p>
        <p className="photoDesc">{data.description} </p>

        <p className="photoReactions">
          &#x2764; {data.reactions.like} &#128049; {data.reactions.macka}{" "}
          &#128054; {data.reactions.doggo}
          &#127788;
        </p>
        {/* <br /> */}
        {/* <br /> */}
      </div>
    </div>
  );
  return item;
}
