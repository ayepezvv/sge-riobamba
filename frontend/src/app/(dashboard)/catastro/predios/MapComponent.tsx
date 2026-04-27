'use client';

import { MapContainer, TileLayer, GeoJSON, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet Default Icon Issue in Next.js
const icon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

function LocationPicker({ position, setPosition }: any) {
  useMapEvents({
    click(e) {
      setPosition([e.latlng.lat, e.latlng.lng]);
    },
  });

  return position === null ? null : (
    <Marker position={position} icon={icon}></Marker>
  );
}

export function PrediosMap({ predios }: { predios: any[] }) {
  // Riobamba center approx
  const center: [number, number] = [-1.6663, -78.6471];

  return (
    <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%', zIndex: 1, borderRadius: 8 }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {predios.map((p) => {
        if (p.geojson) {
          return (
            <GeoJSON 
              key={p.id} 
              data={p.geojson} 
              style={{ color: '#1E88E5', weight: 2 }}
              onEachFeature={(feature, layer) => {
                layer.bindPopup(`<strong>Clave:</strong> ${p.clave_catastral}<br/><strong>Casa:</strong> ${p.numero_casa || 'S/N'}`);
              }}
            />
          );
        }
        return null;
      })}
    </MapContainer>
  );
}

export function MiniMapPicker({ position, setPosition }: { position: any, setPosition: any }) {
  const center: [number, number] = position || [-1.6663, -78.6471];

  return (
    <MapContainer center={center} zoom={15} style={{ height: 250, width: '100%', zIndex: 1, borderRadius: 8, border: '1px solid #e0e0e0' }}>
      <TileLayer
        attribution='&copy; OSM'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LocationPicker position={position} setPosition={setPosition} />
    </MapContainer>
  );
}
