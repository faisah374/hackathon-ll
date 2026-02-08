import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  children: React.ReactNode;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ title, children, className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={`rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden ${className || ''}`}
        {...props}
      >
        {title && (
          <div className="border-b border-gray-200 p-6">
            <h3 className="font-semibold leading-none tracking-tight">{title}</h3>
          </div>
        )}
        <div className="p-6 pt-0">{children}</div>
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card };