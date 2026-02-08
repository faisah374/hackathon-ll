
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AuthProvider } from "@/providers/auth-provider";
import { TodoProvider } from "@/providers/todo-provider";
import {UIProvider} from"@/providers/ui-provider";
import ErrorBoundary from "@/components/common/error-boundary";




const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Todo App",
  description: "A simple todo application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorBoundary>
          <AuthProvider>
            <TodoProvider>
              <UIProvider>
                {children}
              </UIProvider>
            </TodoProvider>
          </AuthProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}