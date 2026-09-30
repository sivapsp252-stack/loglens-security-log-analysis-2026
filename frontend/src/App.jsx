import { useEffect, useState } from "react";

import {
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

function App() {
  const [data, setData] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  // Load normal sample log
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/analysis")
      .then((response) => response.json())
      .then((result) => setData(result))
      .catch((error) => console.error("API Error:", error));
  }, []);

  // Load demo log
  const loadDemoLog = () => {
    fetch("http://127.0.0.1:5000/api/demo-analysis")
      .then((response) => response.json())
      .then((result) => setData(result))
      .catch((error) => console.error("Demo Log Error:", error));
  };

  // Upload custom log and poll background job
  const uploadLog = () => {
    if (!selectedFile) {
      alert("Please select a log file");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:5000/api/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((job) => {
        const jobId = job.job_id;

        const checkJob = () => {
          fetch(`http://127.0.0.1:5000/api/job/${jobId}`)
            .then((response) => response.json())
            .then((result) => {
              if (result.status === "completed") {
                setData(result.result);
                return;
              }

              if (result.status === "failed") {
                alert(`Analysis failed: ${result.error}`);
                return;
              }

              setTimeout(checkJob, 1000);
            })
            .catch((error) => {
              console.error("Job Status Error:", error);
            });
        };

        checkJob();
      })
      .catch((error) => {
        console.error("Upload Error:", error);
      });
  };

  // Loading screen
  if (!data) {
    return <h2>Loading LogLens...</h2>;
  }

  // Attacks per hour chart data
  const chartData = Object.entries(
    data?.attacks_per_hour || {}
  ).map(([hour, attacks]) => ({
    hour: `${hour}:00`,
    attacks,
  }));

  // Attack type chart data
  const attackTypeData = Object.entries(
    data?.attack_types || {}
  ).map(([type, count]) => ({
    name: type.replaceAll("_", " "),
    value: count,
  }));

  // GeoIP map data
  const geoLocations = data?.geo_locations || [];

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial",
        backgroundColor: "#f5f7fb",
        minHeight: "100vh",
      }}
    >
      <h1>🔐 LogLens Security Dashboard</h1>

      <p>Simplified Security Log Analysis</p>

      {/* Demo button */}
      <button
        onClick={loadDemoLog}
        style={{
          marginTop: "15px",
          padding: "12px 20px",
          borderRadius: "8px",
          border: "none",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Load Demo Log
      </button>

      {/* Upload section */}
      <div style={{ marginTop: "15px" }}>
        <input
          type="file"
          accept=".log"
          onChange={(event) =>
            setSelectedFile(event.target.files[0])
          }
        />

        <button
          onClick={uploadLog}
          style={{
            marginLeft: "10px",
            padding: "10px 18px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Upload Log
        </button>
      </div>

      {/* Summary cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <div
          style={{
            background: "white",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <h3>Total Requests</h3>
          <h2>{data.total_requests}</h2>
        </div>

        <div
          style={{
            background: "white",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <h3>Total Attacks</h3>
          <h2>{data.total_attacks}</h2>
        </div>

        <div
          style={{
            background: "white",
            padding: "25px",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <h3>Attack Rate</h3>

          <h2>
            {data.total_requests
              ? Math.round(
                  (data.total_attacks /
                    data.total_requests) *
                    100
                )
              : 0}
            %
          </h2>
        </div>
      </div>

      {/* Attack Types */}
      <h2 style={{ marginTop: "40px" }}>
        Attack Types
      </h2>

      <div
        style={{
          width: "100%",
          height: 350,
          background: "white",
          borderRadius: "12px",
          padding: "10px",
        }}
      >
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={attackTypeData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={120}
              label
            >
              {attackTypeData.map((entry, index) => (
                <Cell key={`cell-${index}`} />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Attacks Per Hour */}
      <h2 style={{ marginTop: "40px" }}>
        Attacks Per Hour
      </h2>

      <div
        style={{
          width: "100%",
          height: 300,
          background: "white",
          borderRadius: "12px",
          padding: "10px",
        }}
      >
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="hour" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="attacks"
              stroke="#2563eb"
              strokeWidth={3}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* GeoIP Map */}
      <h2 style={{ marginTop: "40px" }}>
        🌍 GeoIP Attack Map
      </h2>

      <div
        style={{
          width: "100%",
          height: "450px",
          background: "white",
          borderRadius: "12px",
          overflow: "hidden",
        }}
      >
        {geoLocations.length > 0 ? (
          <MapContainer
            center={[20, 0]}
            zoom={2}
            style={{
              width: "100%",
              height: "100%",
            }}
          >
            <TileLayer
              attribution="&copy; OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {geoLocations.map((location) => (
              <CircleMarker
                key={`${location.ip}-${location.latitude}-${location.longitude}`}
                center={[
                  location.latitude,
                  location.longitude,
                ]}
                radius={10}
              >
                <Popup>
                  <strong>IP:</strong>{" "}
                  {location.ip}

                  <br />

                  <strong>Country:</strong>{" "}
                  {location.country || "Unknown"}

                  <br />

                  <strong>City:</strong>{" "}
                  {location.city || "Unknown"}
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        ) : (
          <div
            style={{
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            No public IP geolocation data available.
          </div>
        )}
      </div>

      {/* Top Attackers */}
      <h2 style={{ marginTop: "40px" }}>
        Top Attackers
      </h2>

      <table
        border="1"
        cellPadding="10"
        style={{
          background: "white",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th>IP Address</th>
            <th>Attack Count</th>
          </tr>
        </thead>

        <tbody>
          {data.top_attackers.map(
            ([ip, count]) => (
              <tr key={ip}>
                <td>{ip}</td>
                <td>{count}</td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;