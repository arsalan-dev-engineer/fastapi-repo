
import { useState } from "react";
import Styles from "./VehicleForm.module.css";

export default function VehicleForm() {
  // define state for each field
  const [formData, setFormData] = useState({
    make: "",
    model: "",
    year: "",
    colour: "",
    body: "",
    doors: "",
    transmission: "",
    engineSize: "",
    fuel: "",
  });

  // helper to update state
  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  // handle form submission
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/vehicles/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const result = await response.json();
      console.log("Success:", result);
      // optional: reset form
      setFormData({
        make: "",
        model: "",
        year: "",
        colour: "",
        body: "",
        doors: "",
        transmission: "",
        engineSize: "",
        fuel: "",
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // define fields with optional select options
  const fields = [
    { id: "make", label: "Make", type: "text" },
    { id: "model", label: "Model", type: "text" },
    { id: "year", label: "Year", type: "number", min: 1900, max: 2099 },
    { id: "colour", label: "Colour", type: "text" },
    {
      id: "body",
      label: "Body",
      type: "select",
      options: ["Sedan", "SUV", "Hatchback", "Coupe", "Convertible"],
    },
    { id: "doors", label: "Doors", type: "number", min: 2, max: 6 },
    {
      id: "transmission",
      label: "Transmission",
      type: "select",
      options: ["Manual", "Automatic", "Semi-Auto"],
    },
    { id: "engineSize", label: "Engine Size (L)", type: "number", min: 0.8, max: 8 },
    {
      id: "fuel",
      label: "Fuel",
      type: "select",
      options: ["Petrol", "Diesel", "Electric", "Hybrid", "CNG"],
    },
  ];

  return (
    <div className={`container-xl ${Styles.pageContainer}`}>
      <form onSubmit={handleSubmit} className={Styles.formContainer}>
        <h1 className="heading--primary">Tell Us About Your Vehicle</h1>

        <div className="row g-3">
          {fields.map((field) => (
            <div className="col-12 col-sm-4" key={field.id}>
              <label htmlFor={field.id} className={Styles.formLabel}>
                {field.label}
              </label>

              {field.type === "select" ? (
                <select
                  id={field.id}
                  className={`form-control ${Styles.formControl}`}
                  value={formData[field.id as keyof typeof formData]}
                  onChange={(e) => handleChange(field.id, e.target.value)}
                  required>
                  <option value="">Select {field.label}</option>
                  {field.options!.map((opt) => (
                    <option key={opt} value={opt}>
                      {opt}
                    </option>
                  ))}
                </select>

              ) : (
                <input
                  id={field.id}
                  type={field.type}
                  min={field.min}
                  max={field.max}
                  className={`form-control ${Styles.formControl}`}
                  placeholder={field.label}
                  value={formData[field.id as keyof typeof formData]}
                  onChange={(e) => handleChange(field.id, e.target.value)}
                  required />
              )}
            </div>
          ))}
        </div>

        <button type="submit" className={Styles.btnSubmit}>
          Submit
        </button>
      </form>
    </div>
  );
}
