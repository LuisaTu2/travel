export default function Photo({ data }) {
  const item = (
    <div>
      <p>{data.title}</p>
      <p>{data.description} </p>
      <img src={data.link} width="500px" />
      <p>
        &#x2764; {data.reactions.like} &#128049; {data.reactions.macka}{" "}
        &#128054; {data.reactions.doggo}
        &#127788;
      </p>
      <br />
      <>*************</>
      <br />
    </div>
  );
  return item;
}
