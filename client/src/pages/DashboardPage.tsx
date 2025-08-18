import { useState, useEffect } from "react";
import axios from "axios";
import type { UserData } from "../types/Interface";
import "../styles/DashboardPage.css";

interface Course {
  id: number;
  courseNumber: string;
  courseName: string;
  status: "available" | "unavailable";
  trackingStatus: "tracking" | "paused" | "stopped";
  crn: string;
  year: number;
  semester: string;
}

interface DashboardPageProps {
  user: UserData | null;
  onLogout: () => void;
}

function DashboardPage({ user, onLogout }: DashboardPageProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    subject_code: "",
    course_number: "",
    crn: "",
    year: new Date().getFullYear(),
    semester: "FALL",
  });

  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  // fetch user sections
  useEffect(() => {
    if (user?.id) {
      fetchUserSections();
    }
  }, [user]);

  const fetchUserSections = async () => {
    if (!user?.id) return;

    try {
      setLoading(true);
      const response = await axios.get(
        `http://localhost:8000/sections/${user.id}`
      );

      const sections = response.data;
      const transformedCourses = sections.map((section: any) => ({
        id: section.id,
        courseNumber: `${section.subject_code} ${section.course_number}`,
        courseName: "Course Name", // temporary for now, need to get the full name
        status: section.is_available ? "available" : "unavailable",
        trackingStatus: section.notifications_enabled ? "tracking" : "paused",
        crn: section.crn,
        year: section.year,
        semester: section.semester,
      }));
      setCourses(transformedCourses);
    } catch (error) {
      console.error("Error fetching sections:", error);
    } finally {
      setLoading(false);
    }
  };

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => {
    setIsModalOpen(false);
    setFormData({
      subject_code: "",
      course_number: "",
      crn: "",
      year: new Date().getFullYear(),
      semester: "FALL",
    });
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "year" ? parseInt(value) || new Date().getFullYear() : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user?.id) {
      console.error("User ID not available");
      return;
    }

    const sectionData = {
      user_id: user.id,
      subject_code: formData.subject_code.toUpperCase(),
      course_number: formData.course_number,
      crn: formData.crn,
      year: formData.year,
      semester: formData.semester,
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/add_section",
        sectionData
      );

      console.log("Section added successfully:", response.data);
      alert("Section added successfully");
      closeModal();
      // refresh section list after adding
      await fetchUserSections();
    } catch (error) {
      console.error("Error adding section:", error);
      if (axios.isAxiosError(error)) {
        const errorMessage =
          error.response?.data?.detail || "Failed to add section";
        alert(`Error: ${errorMessage}`);
      } else {
        alert("Network error occurred. Please try again.");
      }
    }
  };

  const handleDeleteCourse = async (courseId: number) => {
    try {
      await axios.delete(`http://localhost:8000/sections/${courseId}`);

      console.log("Section deleted successfully");
      // refresh section list after deletion
      await fetchUserSections();
    } catch (error) {
      console.error("Error deleting section:", error);
      if (axios.isAxiosError(error)) {
        const errorMessage =
          error.response?.data?.detail || "Failed to delete section";
        alert(`Error: ${errorMessage}`);
      } else {
        alert("Network error occurred. Please try again.");
      }
    }
  };

  const handleStartTracking = (courseId: number) => {
    setCourses((prev) =>
      prev.map((course) =>
        course.id === courseId
          ? { ...course, trackingStatus: "tracking" }
          : course
      )
    );
  };

  const handlePauseTracking = (courseId: number) => {
    setCourses((prev) =>
      prev.map((course) =>
        course.id === courseId
          ? { ...course, trackingStatus: "paused" }
          : course
      )
    );
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1 className="dashboard-title">HokieTracker</h1>
        <button className="logout-button" onClick={onLogout}>
          Logout
        </button>
      </div>
      <div className="dashboard-content">
        <h2>Welcome, {user?.email}</h2>
        <button className="open-modal-button" onClick={openModal}>
          Add Section
        </button>

        <div className="courses-table-container">
          {loading ? (
            <div
              style={{ textAlign: "center", padding: "20px", color: "#ccc" }}
            >
              Loading your sections...
            </div>
          ) : courses.length === 0 ? (
            <div
              style={{ textAlign: "center", padding: "20px", color: "#ccc" }}
            >
              No sections tracked yet. Add a section to get started!
            </div>
          ) : (
            <table className="courses-table">
              <thead>
                <tr>
                  <th>Course</th>
                  <th>CRN</th>
                  <th>Term</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr key={course.id}>
                    <td className="course-info">
                      <div className="course-number">{course.courseNumber}</div>
                      <div className="course-name">{course.courseName}</div>
                    </td>
                    <td>{course.crn}</td>
                    <td>
                      {course.semester} {course.year}
                    </td>
                    <td>
                      <span className={`status-badge ${course.status}`}>
                        {course.status}
                      </span>
                    </td>
                    <td className="actions-cell">
                      <div className="action-buttons">
                        {course.trackingStatus === "tracking" ? (
                          <button
                            className="action-btn pause-btn"
                            onClick={() => handlePauseTracking(course.id)}
                            title="Pause tracking"
                          >
                            ⏸
                          </button>
                        ) : (
                          <button
                            className="action-btn play-btn"
                            onClick={() => handleStartTracking(course.id)}
                            title="Start tracking"
                          >
                            ▶
                          </button>
                        )}
                        <button
                          className="action-btn delete-btn"
                          onClick={() => handleDeleteCourse(course.id)}
                          title="Delete course"
                        >
                          🗑
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {isModalOpen && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Section</h3>
              <button className="close-button" onClick={closeModal}>
                ×
              </button>
            </div>
            <form className="modal-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="text"
                  name="subject_code"
                  placeholder="Subject Code (e.g., CS)"
                  className="modal-input"
                  value={formData.subject_code}
                  onChange={handleInputChange}
                  required
                  maxLength={4}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  name="course_number"
                  placeholder="Course Number (e.g., 3114)"
                  className="modal-input"
                  value={formData.course_number}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  name="crn"
                  placeholder="CRN (5-digit number)"
                  className="modal-input"
                  value={formData.crn}
                  onChange={handleInputChange}
                  required
                  pattern="[0-9]{5}"
                  maxLength={5}
                />
              </div>
              <div className="form-group">
                <input
                  type="number"
                  name="year"
                  placeholder="Year (e.g., 2025)"
                  className="modal-input"
                  value={formData.year}
                  onChange={handleInputChange}
                  required
                  min="2020"
                  max="2030"
                />
              </div>
              <div className="form-group">
                <select
                  name="semester"
                  className="modal-input"
                  value={formData.semester}
                  onChange={handleInputChange}
                  required
                >
                  <option value="FALL">Fall</option>
                  <option value="SPRING">Spring</option>
                  <option value="SUMMER">Summer</option>
                  <option value="WINTER">Winter</option>
                </select>
              </div>
              <div className="modal-buttons">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeModal}
                >
                  Cancel
                </button>
                <button type="submit" className="submit-button">
                  Add Section
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default DashboardPage;
