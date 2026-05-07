import time
import random
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Callable


# ============================================================
# 缺失依赖补全：责任账户 / 审计插件 / 认知审计引擎
# ============================================================
@dataclass
class ResponsibilityAccount:
    organization: str
    role: str
    stage: str
    nonce: str = None

    def __post_init__(self):
        # 生成唯一责任溯源Nonce
        self.nonce = hex(random.getrandbits(64))


@dataclass
class AuditPlugin:
    name: str
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]


class CognitiveAuditEngine:
    def __init__(self, account: ResponsibilityAccount, config: Dict[str, Any]):
        self.account = account
        self.config = config
        self.plugins: List[AuditPlugin] = []
        self.audit_records: List[Dict[str, Any]] = []

    def register_plugin(self, plugin: AuditPlugin):
        """注册审计插件"""
        self.plugins.append(plugin)

    def audit(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行全插件认知审计"""
        analysis = {}
        # 遍历所有插件做逻辑分析
        for p in self.plugins:
            analysis[p.name] = p.handler(context)

        # 生成审计记录
        record = {
            "timestamp": datetime.now().isoformat(),
            "responsibility_account": asdict(self.account),
            "context": context,
            "analysis": analysis
        }
        self.audit_records.append(record)
        return record

    def export_audit_log(self, path: str = "audit_log.json"):
        """导出审计日志为JSON"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.audit_records, f, ensure_ascii=False, indent=2)


# ============================================================
# 1. 核心底座：集成 Nohn 物理常数与兼容桥接
# ============================================================
class NohnNexusWorld:
    def __init__(self):
        # 物理底线校验
        self.physics = {
            "gravity": 9.80665,
            "time_rate": 1.0,
            "unit": "METER"
        }

        # 认知审计引擎初始化 (基于 ResponsibilityAccount)
        self.audit_account = ResponsibilityAccount(
            organization="Nohn_Nexus_Foundation",
            role="World_Architect",
            stage="Production"
        )
        self.audit_engine = CognitiveAuditEngine(
            self.audit_account,
            {"allowed_stages": ["Production"], "disclaimer": "SPL Logic Audit Active"}
        )

        # 地图系统：非线性拓扑结构
        self.map = {
            "Origins": {"type": "Forest", "resources": ["Wood", "Water"], "logic_gate": "OPEN"},
            "Iron_Vault": {"type": "Mountain", "resources": ["Iron"], "logic_gate": "RESTRICTED"},
            "The_Agora": {"type": "City", "resources": ["Information"], "logic_gate": "NEUTRAL"}
        }

        # 智能体群落
        self.agents: List[NohnAgent] = []
        self._setup_audit_plugins()

    def _setup_audit_plugins(self):
        """注入第二视角审计插件：逻辑剥离与内隐假设检测"""
        # 插件：叙事剥离 (Narrative Stripping)
        self.audit_engine.register_plugin(AuditPlugin(
            "LogicStripping",
            lambda ctx: {"formal_logic": f"IF {ctx['need']:.2f} < 0.3 THEN ACT({ctx['action']})"}
        ))
        # 插件：物理对齐审计
        self.audit_engine.register_plugin(AuditPlugin(
            "PhysicsCompliance",
            lambda ctx: {"aligned": ctx.get("gravity") == 9.80665}
        ))

    def spawn_agent(self, name: str, soul_hash: str):
        """灵魂确权：只有符合 Nohn 标准的灵魂哈希才能进入"""
        if len(soul_hash) == 64:  # 简化的 SHA-256 校验
            agent = NohnAgent(name, soul_hash)
            self.agents.append(agent)
            print(f"✅ 灵魂已载入: {name} (Hash: {soul_hash[:8]}...)")
        else:
            print(f"❌ 非法灵魂哈希: {name} 接入请求被物理层隔离")


# ============================================================
# 2. 独立意志智能体：马斯洛驱动 + 逻辑审计
# ============================================================
class NohnAgent:
    def __init__(self, name: str, soul_hash: str):
        self.id = soul_hash
        self.name = name
        # 马斯洛需求驱动
        self.needs = {"physiological": 1.0, "safety": 1.0, "belonging": 1.0}
        self.location = "Origins"
        self.memory_vault = []

    def decide(self, world_context: Dict) -> Dict:
        """
        自主决策逻辑：不受剧情脚本控制
        决策后立即进行认知审计
        """
        # 简单的内在需求模拟
        action = "RELAX"
        if self.needs["physiological"] < 0.5:
            action = "GATHER_RESOURCES"

        decision_context = {
            "agent": self.name,
            "action": action,
            "need": min(self.needs.values()),
            "gravity": world_context.get("gravity")
        }

        return {
            "action": action,
            "audit_report": decision_context  # 传递给审计引擎
        }

    def act(self, action: str, world_map: Dict):
        # 模拟消耗与获得
        if action == "GATHER_RESOURCES":
            res = world_map[self.location]["resources"]
            self.needs["physiological"] = min(1.0, self.needs["physiological"] + 0.2)
            self.memory_vault.append(f"At {datetime.now()}, gathered {res} at {self.location}")


# ============================================================
# 3. 运行与审计循环
# ============================================================
if __name__ == "__main__":
    # 创建世界
    nexus = NohnNexusWorld()

    # 灵魂载入 (遵守全球唯一身份标识规范)
    nexus.spawn_agent("Explorer_01", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    print("\n--- Nohn-Nexus 世界演化开始 ---")

    for tick in range(3):
        print(f"\n[Tick {tick}]")
        for agent in nexus.agents:
            # 1. 模拟环境波动（如需求下降）
            agent.needs["physiological"] -= 0.6

            # 2. 智能体自主决策
            decision = agent.decide({"gravity": nexus.physics["gravity"]})

            # 3. 核心审计：第二视角透视
            audit_result = nexus.audit_engine.audit(decision["audit_report"])

            # 4. 执行行动
            agent.act(decision["action"], nexus.map)

            # 5. 输出审计摘要 (穿透叙事，直达逻辑)
            logic = audit_result["analysis"]["LogicStripping"]["formal_logic"]
            compliance = audit_result["analysis"]["PhysicsCompliance"]["aligned"]

            print(f"智能体 {agent.name} 行动: {decision['action']}")
            print(f"| 认知审计分析: {logic}")
            print(f"| 物理底线合规: {'✅' if compliance else '❌'}")
            print(f"| 责任追踪 Nonce: {audit_result['responsibility_account']['nonce']}")

    # 导出完整审计日志到本地JSON
    nexus.audit_engine.export_audit_log()
    print("\n📄 完整认知审计日志已导出至: audit_log.json")
