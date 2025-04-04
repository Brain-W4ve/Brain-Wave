import { useLocation } from 'react-router-dom';
import SciChart from "./SciChart";

function Visualizer() {
  const location = useLocation();
  const data = location.state?.data;

  if (!data) {
    return <div>No data available</div>; // fallback in case of direct access
  }

  return (
    <div className='container mt-5'>
        <SciChart data={data}/>
    </div>
  );
}

export default Visualizer;
