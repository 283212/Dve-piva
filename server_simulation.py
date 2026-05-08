

if __name__ == "__main__":
    tasks = [
        {"task_id": 1, "name": "Simulation", "threads": 4, "memory": 8},
        {"task_id": 2, "name": "Rendering", "threads": 2, "memory": 4},
        {"task_id": 3, "name": "AI Training", "threads": 8, "memory": 16},
        {"task_id": 4, "name": "Data Analysis", "threads": 2, "memory": 2},
    ]

class Task:
    def __init__(self, task_id, name, threads, memory):
        self.task_id = task_id
        self.name = name
        self.threads = threads
        self.memory = memory
        self.status = "queued"
        self.remaining_time = threads + memory

    def start(self):
        self.status = "running"

    def complete(self):
        self.status = "completed"

    def compute_step(self):
        if self.status == "running":
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.complete()

    def show_info(self):
        print(f"Task {self.task_id}: {self.name} (Threads: {self.threads}, Memory: {self.memory}GB) - "
              f"Status: {self.status}, remaining time: {self.remaining_time}")




class Server:
    def __init__(self, name, threads, memory):
        self.name = name
        self.threads = threads
        self.memory = memory

        self.queue = []
        self.current_tasks = []
        self.completed_tasks = []


    def add_task(self, task):
        self.queue.append(task)

    def can_run(self, task):
        dostupne = True
        if task.threads > self.threads or task.memory > self.memory:
            dostupne = False
        return dostupne

    def start_task(self, task):
        task.start()
        self.memory -= task.memory
        self.threads -= task.threads
        self.current_tasks.append(task)

    def run_next_task(self):
        if self.queue:
            uloha = self.queue[0]
            if self.can_run(uloha):
                self.queue.pop(0)
                self.start_task(uloha)
                return True                 ##
        return False                        ## fronta je prázdná

    def process_step(self):
        for task in self.current_tasks[:]:
            task.compute_step()
            if task.status == "completed":
                self.current_tasks.remove(task)
                self.completed_tasks.append(task)
                self.threads += task.threads
                self.memory += task.memory
        #self.run_next_task()

        while self.run_next_task():   ## Pokud jsou ve frontě další úlohy (while True),
            pass             ## pokusí se spustit další úlohu pomocí run_next_task()


    def show_status(self):
        jmena_bezicich_uloh = []

        for task in self.current_tasks:
            jmena_bezicich_uloh.append(task.name)

        running_names = ", ".join(jmena_bezicich_uloh)     #z ["A", "B"] udělá "A, B"

        if not running_names:                          # pokud je seznam prazdny, test chce vypsat "Running: None"
            running_names = "None"

        print(f"Server {self.name} - Running: {running_names} (Threads: {self.threads}, Memory: {self.memory}GB), Queue: {len(self.queue)} tasks")




def main(name, threads, memory, task_list, steps):

    server = Server(name, threads, memory)

    for uloha in task_list:
        nova_uloha = Task(uloha["task_id"], uloha["name"], uloha["threads"], uloha["memory"])
        server.add_task(nova_uloha)

    server.show_status()

    for i in range(steps):
        server.process_step()
        server.show_status()

    return server.completed_tasks
