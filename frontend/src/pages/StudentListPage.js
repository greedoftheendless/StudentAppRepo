import React, { useEffect, useState } from "react";
import api from "../services/api";

export default function StudentListPage() {
  const [students, setStudents] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const res = await api.get("/api/students/");
        setStudents(res.data);
      } catch (err) {
        setError("Failed to load students");
      }
    };
    fetchStudents();
  }, []);

  return (
    <div className="card">
      <h2>Student List</h2>
      {error && <p className="error">{error}</p>}
      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id}>
                <td>{s.id}</td>
                <td>{s.name}</td>
                <td>{s.age}</td>
                <td>{s.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
