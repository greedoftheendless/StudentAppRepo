import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import LoginPage from "./LoginPage";
import api from "../services/api";

// Mock the api module
jest.mock("../services/api");

const renderLogin = () =>
  render(
    <MemoryRouter>
      <LoginPage />
    </MemoryRouter>
  );

test("renders login form with username and password fields", () => {
  renderLogin();
  expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
});

test("shows error on failed login", async () => {
  api.post.mockRejectedValue({
    response: { data: { detail: "Invalid credentials" } },
  });
  renderLogin();

  fireEvent.change(screen.getByLabelText(/username/i), {
    target: { value: "bad" },
  });
  fireEvent.change(screen.getByLabelText(/password/i), {
    target: { value: "wrong" },
  });
  fireEvent.click(screen.getByRole("button", { name: /login/i }));

  await waitFor(() => {
    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
  });
});

test("toggles between login and register mode", () => {
  renderLogin();
  fireEvent.click(screen.getByRole("button", { name: /register/i }));
  expect(screen.getByRole("heading", { name: /register/i })).toBeInTheDocument();
});
