// app/page.tsx
"use client";

import { WeatherForm } from "@/components/weather-form";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  const [lookupId, setLookupId] = useState("");
  const [weatherData, setWeatherData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLookup = async () => {
    if (!lookupId.trim()) {
      setError("Please enter a request ID");
      return;
    }

    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch(`http://localhost:8000/weather/${lookupId}`);
      if (!response.ok) {
        throw new Error("Weather data not found");
      }
      const data = await response.json();
      setWeatherData(data);
    } catch (err: any) {
      setError(err.message);
      setWeatherData(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Weather System
          </h1>
          <p className="text-muted-foreground text-lg">
            Submit weather requests and retrieve stored results
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          {/* Weather Form Section */}
          <div>
            <h2 className="text-2xl font-semibold mb-4">
              Submit Weather Request
            </h2>
            <WeatherForm />
          </div>

          {/* Data Lookup Section */}
          <div>
            <h2 className="text-2xl font-semibold mb-4">Lookup Weather Data</h2>
            <Card>
              <CardHeader>
                <CardTitle>Retrieve Weather Data</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input
                    placeholder="Enter request ID"
                    value={lookupId}
                    onChange={(e) => setLookupId(e.target.value)}
                  />
                  <Button 
                    onClick={handleLookup} 
                    disabled={isLoading}
                  >
                    {isLoading ? "Searching..." : "Search"}
                  </Button>
                </div>
                
                {error && (
                  <div className="text-red-500 text-sm">{error}</div>
                )}

                {weatherData && (
                  <div className="mt-4 space-y-2">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <p className="text-sm text-muted-foreground">Date</p>
                        <p>{weatherData.date}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Location</p>
                        <p>{weatherData.location}</p>
                      </div>
                    </div>
                    {weatherData.notes && (
                      <div>
                        <p className="text-sm text-muted-foreground">Notes</p>
                        <p>{weatherData.notes}</p>
                      </div>
                    )}
                    <div className="pt-4">
                      <p className="text-sm text-muted-foreground">Weather Data</p>
                      <pre className="text-xs bg-muted p-2 rounded overflow-auto">
                        {JSON.stringify(weatherData.weather_data, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}