interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className = '' }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse bg-slate-800 rounded-lg ${className}`}
    />
  );
}

export function ChartSkeleton() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-3 shadow-xl">
      <Skeleton className="h-5 w-40" />
      <Skeleton className="h-[340px] w-full" />
    </div>
  );
}

export function SignalCardSkeleton() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5 shadow-xl">
      <div className="flex flex-col items-center gap-3">
        <Skeleton className="h-3 w-24" />
        <Skeleton className="h-20 w-56" />
        <Skeleton className="h-2 w-full" />
      </div>
      <div className="grid grid-cols-2 gap-3 pt-4 border-t border-slate-800">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="space-y-1">
            <Skeleton className="h-2.5 w-16" />
            <Skeleton className="h-4 w-24" />
          </div>
        ))}
      </div>
    </div>
  );
}
