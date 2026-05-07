import time, random, json, uuid, tkinter as tk
from tkinter import ttk
from datetime import datetime
from dataclasses import dataclass

# ==============================================
# 1. 核心框架：认知审计引擎 (Cognitive Audit Engine)
# ==============================================
@dataclass
class ResponsibilityAccount:
    organization: str; role: str; stage: str; nonce: str = None
    def __post_init__(self): 
        if not self.nonce: self.nonce = uuid.uuid4().hex[:8]

class AuditPlugin:
    def __init__(self, name, analyze_func):
        self.name, self.analyze = name, analyze_func

class CognitiveAuditEngine:
    def __init__(self, account, config):
        self.account, self.config, self.plugins = account, config, []
    def register_plugin(self, plugin): self.plugins.append(plugin)
    def audit(self, ctx):
        report = {"account": self.account.__dict__, "analysis": {}}
        for p in self.plugins: report["analysis"][p.name] = p.analyze(ctx)
        return report

# ==============================================
# 2. 深度功能模块：经济、任务与动态地图
# ==============================================
class EconomySystem:
    """经济系统：货币与物价逻辑"""
    def __init__(self):
        self.currency = "NOHN-COIN"
        self.prices = {"Bread": 10, "Iron": 50}

class TaskGenerator:
    """自动任务系统：基于智能体需求涌现任务"""
    @staticmethod
    def generate(agent):
        if agent.needs["food"] < 0.5:
            return {"type": "GATHER", "target": "Origins", "reward": 20}
        if agent.wallet < 10:
            return {"type": "WORK", "target": "Iron_Vault", "reward_coin": 15}
        return {"type": "EXPLORE", "target": "The_Agora", "reward": 5}

# ==============================================
# 3. 智能体与世界集成
# ==============================================
class NohnAgent:
    def __init__(self, name, soul_hash):
        self.name, self.id = name, soul_hash
        self.needs = {"food": 0.8, "safety": 1.0}
        self.wallet = 20  # 初始货币
        self.location = "Origins"
        self.current_task = None

    def decide(self):
        # 自动任务生成替代了简单的手动决策
        self.current_task = TaskGenerator.generate(self)
        return {
            "task": self.current_task["type"],
            "target": self.current_task["target"],
            "logic_ctx": {
                "agent": self.name,
                "need_level": self.needs["food"],
                "wealth": self.wallet,
                "action": self.current_task["type"]
            }
        }

class NohnWorld:
    def __init__(self):
        self.physics = {"gravity": 9.80665}
        self.economy = EconomySystem()
        self.map = {
            "Origins": {"color": "#A8E6CF", "pos": (100, 100, 250, 250), "res": "Food"},
            "Iron_Vault": {"color": "#DCEDC1", "pos": (280, 100, 430, 250), "res": "Iron"},
            "The_Agora": {"color": "#FFD3B6", "pos": (460, 100, 610, 250), "res": "Coin"}
        }
        self.agents = []
        # 初始化审计
        acc = ResponsibilityAccount("Nohn_Foundation", "Architect", "Production")
        self.engine = CognitiveAuditEngine(acc, {"allowed_stages": ["Production"]})
        self.engine.register_plugin(AuditPlugin("NarrativeStripping", 
            lambda c: {"logic": f"NEED({c['need_level']:.2f}) + WEALTH({c['wealth']}) -> {c['action']}"}))

    def spawn(self, name, soul_hash):
        if len(soul_hash) == 64: self.agents.append(NohnAgent(name, soul_hash))

# ==============================================
# 4. 视觉渲染与审计交互
# ==============================================
class NohnVisualApp:
    def __init__(self, world):
        self.world = world
        self.root = tk.Tk()
        self.root.title("NOHN 虚拟世界 - 社会演化审计版")
        self.canvas = tk.Canvas(self.root, width=700, height=450, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10)
        self.audit_log = tk.Text(self.root, width=45, height=30, font=("Consolas", 9))
        self.audit_log.pack(side=tk.RIGHT, padx=10)
        ttk.Button(self.root, text="推进世界演化 (Tick)", command=self.step).pack(pady=10)
        self.draw_map()

    def draw_map(self):
        for n, d in self.world.map.items():
            self.canvas.create_rectangle(*d['pos'], fill=d['color'], outline="white")
            self.canvas.create_text(d['pos'][0]+75, d['pos'][1]-10, text=f"{n}\n({d['res']})", font=("Arial", 9))

    def step(self):
        self.canvas.delete("agent")
        for a in self.world.agents:
            a.needs["food"] -= 0.2 # 熵增：饥饿感增加
            decision = a.decide()
            report = self.world.engine.audit(decision["logic_ctx"])
            
            # 执行任务逻辑
            a.location = decision["target"]
            if decision["task"] == "GATHER": a.needs["food"] = 1.0
            if decision["task"] == "WORK": a.wallet += 15
            
            # 渲染
            x1, y1, x2, y2 = self.world.map[a.location]["pos"]
            self.canvas.create_oval((x1+x2)/2-15, (y1+y2)/2-15, (x1+x2)/2+15, (y1+y2)/2+15, fill="#FF8B94", tags="agent")
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2+25, text=f"{a.name}\n${a.wallet}", tags="agent", font=("Arial", 8))
            
            # 审计输出
            self.audit_log.insert(tk.END, f"审计对象: {a.name} | Nonce: {report['account']['nonce']}\n")
            self.audit_log.insert(tk.END, f"└─ 剥离逻辑: {report['analysis']['NarrativeStripping']['logic']}\n\n")
            self.audit_log.see(tk.END)

if __name__ == "__main__":
    nexus = NohnWorld()
    nexus.spawn("Explorer_01", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    nexus.spawn("Merchant_02", "f8e2c3a1b0d9e8f7c6b5a4938271605b4a3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e")
    NohnVisualApp(nexus).root.mainloop()
