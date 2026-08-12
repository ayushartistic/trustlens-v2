import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Posts from "./pages/Posts";
import Comments from "./pages/Comments";
import Accounts from "./pages/Accounts";
import Detections from "./pages/Detections";
import Attacks from "./pages/Attacks";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route element={<MainLayout />}>

          <Route path="/" element={<Dashboard />} />

          <Route path="/users" element={<Users />} />

          <Route path="/posts" element={<Posts />} />

          <Route path="/comments" element={<Comments />} />

          <Route path="/accounts" element={<Accounts />} />

          <Route path="/detections" element={<Detections />} />

          <Route path="/attacks" element={<Attacks />} />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;