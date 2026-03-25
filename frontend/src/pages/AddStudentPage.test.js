import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import AddStudentPage from "./AddStudentPage";
import api from "../services/api";

jest.mock("../services/api");

const renderPage = () =>
  render(
    <MemoryRouter>
      <AddStudentPage />
    </MemoryRouter>
  );

test("renders add student form", () => {
  renderPage();
  expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/age/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /add student/i })).toBeInTheDocument();
});

test("submits form successfully", async () => {
  api.post.mockResolvedValue({ data: { id: 1, name: "Alice", age: 20, email: "a@b.com" } });
  renderPage();

  fireEvent.change(screen.getByLabelText(/name/i), { target: { value: "Alice" } });
  fireEvent.change(screen.getByLabelText(/age/i), { target: { value: "20" } });
  fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "a@b.com" } });
  fireEvent.click(screen.getByRole("button", { name: /add student/i }));

  await waitFor(() => {
    expect(screen.getByText(/student added successfully/i)).toBeInTheDocument();
  });
});

test("shows error on failed submission", async () => {
  api.post.mockRejectedValue({
    response: { data: { detail: "Email already registered" } },
  });
  renderPage();

  fireEvent.change(screen.getByLabelText(/name/i), { target: { value: "Bob" } });
  fireEvent.change(screen.getByLabelText(/age/i), { target: { value: "22" } });
  fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "dup@b.com" } });
  fireEvent.click(screen.getByRole("button", { name: /add student/i }));

  await waitFor(() => {
    expect(screen.getByText(/email already registered/i)).toBeInTheDocument();
  });
});
