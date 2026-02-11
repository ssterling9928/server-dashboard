
import { useState, useEffect, useCallback } from "react";
import { Service, ServicesResponse } from "../types/services";
import ServiceGrid from "../css/ServiceGrid.css";

export function useServices() { 
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(async () => {
    setLoading(true);
    try {
      const r = await fetch("/api/services");
      const data = await r.json() as ServicesResponse;
      setServices(data.data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { services, loading, refetch };
}
