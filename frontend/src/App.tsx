import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Containers from './pages/Containers';
import Rooms from './pages/Rooms';
import Floors from './pages/Floors';
import Items from './pages/Items';
import ContainerDetail from './pages/ContainerDetail';
import RoomDetail from './pages/RoomDetail';
import FloorDetail from './pages/FloorDetail';
import ItemDetail from './pages/ItemDetail';
import Search from './pages/Search';
import ContainerCreate from './pages/ContainerCreate';
import RoomCreate from './pages/RoomCreate';
import FloorCreate from './pages/FloorCreate';
import ItemCreate from './pages/ItemCreate';
import ContainerEdit from './pages/ContainerEdit';
import RoomEdit from './pages/RoomEdit';
import FloorEdit from './pages/FloorEdit';
import ItemEdit from './pages/ItemEdit';
import NotFound from './pages/NotFound';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/items" replace />} />
          <Route path="items" element={<Items />} />
          <Route path="containers" element={<Containers />} />
          <Route path="rooms" element={<Rooms />} />
          <Route path="floors" element={<Floors />} />
          <Route path="items/:id" element={<ItemDetail />} />
          <Route path="containers/:id" element={<ContainerDetail />} />
          <Route path="rooms/:id" element={<RoomDetail />} />
          <Route path="floors/:id" element={<FloorDetail />} />
          <Route path="search" element={<Search />} />
          <Route path="containers/create" element={<ContainerCreate />} />
          <Route path="rooms/create" element={<RoomCreate />} />
          <Route path="floors/create" element={<FloorCreate />} />
          <Route path="items/create" element={<ItemCreate />} />
          <Route path="containers/:id/edit" element={<ContainerEdit />} />
          <Route path="rooms/:id/edit" element={<RoomEdit />} />
          <Route path="floors/:id/edit" element={<FloorEdit />} />
          <Route path="items/:id/edit" element={<ItemEdit />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
