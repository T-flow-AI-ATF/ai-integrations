import React, { useState } from "react";
import { db } from "./firebase";
import { collection, addDoc, updateDoc, deleteDoc, doc, getDocs } from "firebase/firestore";

const SymptomForm = () => {
  const [description, setDescription] = useState("");
  const [symptoms, setSymptoms] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const symptomsRef = collection(db, "symptoms");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (editingId) {
      const docRef = doc(db, "symptoms", editingId);
      await updateDoc(docRef, {
        description,
        timestamp: new Date()
      });
      setEditingId(null);
    } else {
      await addDoc(symptomsRef, {
        description,
        timestamp: new Date()
      });
    }

    setDescription("");
    fetchSymptoms();
  };

  const fetchSymptoms = async () => {
    const data = await getDocs(symptomsRef);
    setSymptoms(data.docs.map(doc => ({ ...doc.data(), id: doc.id })));
  };

  const handleDelete = async (id) => {
    await deleteDoc(doc(db, "symptoms", id));
    fetchSymptoms();
  };

  const handleEdit = (symptom) => {
    setDescription(symptom.description);
    setEditingId(symptom.id);
  };

  React.useEffect(() => {
    fetchSymptoms();
  }, []);

  return (
    <div style={{ maxWidth: "400px", margin: "auto" }}>
      <h2>Symptom Form</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Describe symptom"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        <button type="submit">{editingId ? "Update" : "Add"}</button>
      </form>

      <ul>
        {symptoms.map(symptom => (
          <li key={symptom.id}>
            {symptom.description} <br />
            <button onClick={() => handleEdit(symptom)}>Edit</button>
            <button onClick={() => handleDelete(symptom.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SymptomForm;
