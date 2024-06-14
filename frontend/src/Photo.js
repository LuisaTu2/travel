export default function Photo({ data }) {
  const item = (
    <div>
      <p>{data.title}</p>
      <p>{data.description} </p>
      <img src={data.link} width="200px" />
    </div>
  );
  return item;
}
