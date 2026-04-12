"use client";

import { useCallback, useState } from "react";
import { BenchmarkRun } from "@/lib/types";
import { importJsonFile, addRun } from "@/lib/store";

interface ImportButtonProps {
  onImport: (runs: BenchmarkRun[]) => void;
  runs: BenchmarkRun[];
}

export default function ImportButton({ onImport, runs }: ImportButtonProps) {
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = useCallback(
    async (files: FileList) => {
      setError(null);
      const jsonFiles = Array.from(files).filter(
        (f) => f.name.endsWith(".json") || f.type === "application/json"
      );
      if (jsonFiles.length === 0) {
        setError("No JSON files found");
        return;
      }
      let updated = [...runs];
      for (const file of jsonFiles) {
        try {
          const run = await importJsonFile(file);
          updated = addRun(run);
        } catch (err) {
          setError(err instanceof Error ? err.message : "Import failed");
        }
      }
      onImport(updated);
    },
    [onImport, runs]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      handleFiles(e.dataTransfer.files);
    },
    [handleFiles]
  );

  return (
    <div className="flex flex-col gap-2">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-lg p-4 text-center transition-colors ${
          dragOver
            ? "border-blue-400 bg-blue-50"
            : "border-gray-300 hover:border-gray-400"
        }`}
      >
        <input
          type="file"
          accept=".json"
          multiple
          className="absolute inset-0 opacity-0 cursor-pointer"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />
        <div className="text-sm text-gray-600">
          <span className="font-medium text-blue-600">Click to upload</span>{" "}
          or drag & drop JSON results files
        </div>
      </div>
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
}
