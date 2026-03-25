import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders login page by default when not authenticated", () => {
  localStorage.removeItem("token");
  render(<App />);
  expect(screen.getByRole("heading", { name: /login/i })).toBeInTheDocument();
});
