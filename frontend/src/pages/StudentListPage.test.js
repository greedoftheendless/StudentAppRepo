import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import StudentListPage from "./StudentListPage";
import api from "../services/api";

jest.mock("../services/api");

const renderPage = () =>
  render(
    <MemoryRouter>
      <StudentListPage />
    </MemoryRouter>
  );

test("renders student list heading", () => {
  api.get.mockResolvedValue({ data: [] });
  renderPage();
  expect(screen.getByRole("heading", { name: /student list/i })).toBeInTheDocument();
});

test("shows students in table", async () => {
  api.get.mockResolvedValue({
    data: [
      { id: 1, name: "Alice", age: 20, email: "alice@example.com" },
      { id: 2, name: "Bob", age: 22, email: "bob@example.com" },
    ],
  });
  renderPage();

  await waitFor(() => {
    expect(screen.getByText("Alice")).toBeInTheDocument();
    expect(screen.getByText("Bob")).toBeInTheDocument();
  });
});

test("shows empty message when no students", async () => {
  api.get.mockResolvedValue({ data: [] });
  renderPage();

  await waitFor(() => {
    expect(screen.getByText(/no students found/i)).toBeInTheDocument();
  });
});
