'use client';

import { useState, useCallback } from 'react';

// third party
import { StyleSpecification } from 'maplibre-gl';
import type { Marker } from 'maplibre-gl';
import { Event, RMap, RMarker } from 'maplibre-react-components';

// project imports
import osm_bright from './map-data/osm_bright.json';

// ==============================|| MAPLIBRE - DRAGGABLE MARKER MAP ||============================== //

export default function DraggableMarker() {
  const [marker, setMarker] = useState({ latitude: 21.2335611, longitude: 72.8636084 });

  const onMarkerDrag = useCallback((e: Event<Marker>) => {
    const lngLat = e.target.getLngLat();
    setMarker({ latitude: lngLat.lat, longitude: lngLat.lng });
  }, []);

  const center: [number, number] = [marker.longitude, marker.latitude];

  return (
    <RMap initialCenter={center} initialZoom={4} mapStyle={osm_bright as StyleSpecification}>
      <RMarker longitude={marker.longitude} latitude={marker.latitude} draggable={true} initialAnchor="bottom" onDrag={onMarkerDrag} />
    </RMap>
  );
}
