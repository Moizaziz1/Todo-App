export default function LoadingSkeleton() {
  return (
    <div className="space-y-4" role="status" aria-label="Loading tasks">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="border border-gray-200 rounded-lg p-4 animate-pulse"
        >
          <div className="flex items-start space-x-4">
            <div className="w-5 h-5 bg-gray-200 rounded"></div>
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
