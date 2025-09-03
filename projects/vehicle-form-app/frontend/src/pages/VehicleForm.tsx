import { useState } from 'react';
import Styles from './VehicleForm.module.css';

export default function VehicleForm() {
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [colour, setColour] = useState('');
  const [body, setBody] = useState('');
  const [doors, setDoors] = useState('');
  const [transmission, setTransmission] = useState('');
  const [engineSize, setEngineSize] = useState('');
  const [fuel, setFuel] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const data = {
      make,
      model,
      year,
      colour,
      body,
      doors,
      transmission,
      engineSize,
      fuel,
    };

    try {
      const response = await fetch('http://localhost:8000/vehicle/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('Success:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className={`container-xl bg-light ${Styles.pageContainer}`}>
      <form onSubmit={handleSubmit} className={Styles.formContainer}>
        <h1 className="heading--primary">Tell Us About Your Vehicle</h1>

        {/* row 1 */}
        <div className="row g-3">
          <div className="col-12 col-sm-4">
            <label htmlFor="make" className={Styles.formLabel}>Make</label>
            <input
              id="make"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Make"
              value={make}
              onChange={(e) => setMake(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="model" className={Styles.formLabel}>Model</label>
            <input
              id="model"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="year" className={Styles.formLabel}>Year</label>
            <input
              id="year"
              type="number"
              className={`form-control ${Styles.formControl}`}
              placeholder="Year"
              min="1900"
              max="2099"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              required
            />
          </div>
        </div>

        {/* row 2 */}
        <div className="row g-3">
          <div className="col-12 col-sm-4">
            <label htmlFor="colour" className={Styles.formLabel}>Colour</label>
            <input
              id="colour"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Colour"
              value={colour}
              onChange={(e) => setColour(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="body" className={Styles.formLabel}>Body</label>
            <input
              id="body"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Body Type"
              value={body}
              onChange={(e) => setBody(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="doors" className={Styles.formLabel}>Doors</label>
            <input
              id="doors"
              type="number"
              className={`form-control ${Styles.formControl}`}
              placeholder="Num of Doors"
              value={doors}
              onChange={(e) => setDoors(e.target.value)}
              required
            />
          </div>
        </div>

        {/* row 3 */}
        <div className="row g-3">
          <div className="col-12 col-sm-4">
            <label htmlFor="transmission" className={Styles.formLabel}>Transmission</label>
            <input
              id="transmission"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Transmission Type"
              value={transmission}
              onChange={(e) => setTransmission(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="engineSize" className={Styles.formLabel}>Engine Size</label>
            <input
              id="engineSize"
              type="number"
              className={`form-control ${Styles.formControl}`}
              placeholder="Engine Size"
              value={engineSize}
              onChange={(e) => setEngineSize(e.target.value)}
              required
            />
          </div>

          <div className="col-12 col-sm-4">
            <label htmlFor="fuel" className={Styles.formLabel}>Fuel</label>
            <input
              id="fuel"
              type="text"
              className={`form-control ${Styles.formControl}`}
              placeholder="Fuel Type"
              value={fuel}
              onChange={(e) => setFuel(e.target.value)}
              required
            />
          </div>
        </div>

        <button type="submit" className={Styles.btnSubmit}>Submit</button>
      </form>
    </div>
  );
}
