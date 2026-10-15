// Source: src/LibraryPage.tsx
import { useState } from "react";
import { useTracks } from "./useTracks";
import { TrackList } from "packages/ui/TrackList";

export function LibraryPage() {
  const { tracks } = useTracks();
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <main>
      <TrackList
        tracks={tracks}
        selectedId={selectedId}
        onSelect={setSelectedId}
      />
      <Player trackId={selectedId} />
    </main>
  );
}

function Player({ trackId }: { trackId: string | null }) {
  const [muted, setMuted] = useState(false);
  return (
    <section>
      <audio src={trackId === null ? undefined : `/audio/${trackId}`} muted={muted} controls />
      <button onClick={() => setMuted((value) => !value)}>
        {muted ? "取消静音" : "静音"}
      </button>
    </section>
  );
}
