import { useState, useEffect, useCallback } from "react";
import { Service } from "../types/services";

export function useServices() { 
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  const refetch = useCallback(async () => {
    console.log("🔄 refetch called");
    setLoading(true);
    try {
      const r = await fetch("/api/services");
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json() as Service[];
      console.log("📦 API data:", data);
      setServices(data);
    } catch (error) {
      console.error("💥 Fetch error:", error);
      setServices([]);
    } finally {
      setLoading(false);
    }
  }, []);  


  useEffect(() => {
    console.log("🚀 useEffect running");
    refetch();
  }, []);

  return { services, loading, refetch };
}