import { ReactNode } from 'react';

// project imports
import Kanban from 'views/application/kanban';

// ==============================|| PAGE ||============================== //

export default function KanbanPage({ children }: { children: ReactNode }) {
  return <Kanban>{children}</Kanban>;
}
