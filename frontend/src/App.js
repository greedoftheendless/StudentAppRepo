import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import AddStudentPage from "./pages/AddStudentPage";
import StudentListPage from "./pages/StudentListPage";
import Navbar from "./components/Navbar";
import "./App.css";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route
              path="/add-student"
              element={
                <PrivateRoute>
                  <AddStudentPage />
                </PrivateRoute>
              }
            />
            <Route
              path="/students"
              element={
                <PrivateRoute>
                  <StudentListPage />
                </PrivateRoute>
              }
            />
            <Route path="*" element={<Navigate to="/students" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
