import React, { useState } from "react";
import "./index.css";
import { BrowserRouter, Route, Routes, Link } from "react-router-dom";

import Main from "./components/main.js";
import Result from "./components/results.js";
import CardDetails from "./components/card-detail.js";

function App() {
	return (
		<BrowserRouter>
			<div className="App">
				<Routes>
					<Route path="/" element={<Main />} />
					<Route path="/result" element={<Result />} />
					{/* <Route path="/card/:id" component={CardDetails} /> */}
					<Route path="/card" element={<CardDetails />} />
				</Routes>
			</div>
		</BrowserRouter>
	);
}

export default App;
