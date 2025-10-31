"""
Interactive command-line demo for PROTOCOL:LOOP
"""

import asyncio
import sys
from typing import Dict, Any
from colorama import Fore, Back, Style, init

from backend.services.loop_manager import LoopManager
from backend.services.evolution_engine import EvolutionEngine
from backend.services.llm_service import LLMService
from backend.models.cognitive_state import CognitiveState
from backend.models.memory import MemoryBank

# Initialize colorama
init(autoreset=True)


class InteractiveDemo:
    """Interactive CLI demo for testing PROTOCOL:LOOP"""
    
    def __init__(self):
        self.loop_manager = LoopManager()
        self.evolution_engine = EvolutionEngine()
        self.llm_service = LLMService()
        self.player_id = "demo_player"
        self.cognitive_state = None
        self.memory_bank = None
        self.current_loop = None
        
    def print_header(self):
        """Print demo header"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{Fore.CYAN}█▀█ █▀█ █▀█ ▀█▀ █▀█ █▀▀ █▀█ █░░   ░   █░░ █▀█ █▀█ █▀█")
        print(f"{Fore.CYAN}█▀▀ █▀▄ █▄█ ░█░ █▄█ █▄▄ █▄█ █▄▄   ▄   █▄▄ █▄█ █▄█ █▀▀")
        print(f"{Fore.CYAN}Recursive AI Consciousness Simulator - Interactive Demo")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def print_menu(self):
        """Print main menu"""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== MAIN MENU ==={Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Initialize Player")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Start New Loop")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Generate Protocol")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} View Cognitive State")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} View Evolution Tree")
        print(f"{Fore.GREEN}6.{Style.RESET_ALL} Simulate Decision")
        print(f"{Fore.GREEN}7.{Style.RESET_ALL} Complete Loop")
        print(f"{Fore.GREEN}8.{Style.RESET_ALL} Run Full Simulation")
        print(f"{Fore.GREEN}9.{Style.RESET_ALL} Exit")
        print()
    
    def initialize_player(self):
        """Initialize player state"""
        print(f"\n{Fore.CYAN}Initializing player...{Style.RESET_ALL}")
        
        self.cognitive_state = self.evolution_engine.initialize_cognitive_state(
            self.player_id
        )
        self.memory_bank = MemoryBank(player_id=self.player_id)
        
        print(f"{Fore.GREEN}✓ Player initialized successfully{Style.RESET_ALL}")
        print(f"Player ID: {Fore.YELLOW}{self.player_id}{Style.RESET_ALL}")
        print(f"Initial Evolution Score: {Fore.YELLOW}{self.cognitive_state.evolution_score:.1f}%{Style.RESET_ALL}")
    
    def start_loop(self):
        """Start a new loop"""
        if not self.cognitive_state:
            print(f"{Fore.RED}✗ Please initialize player first{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Starting new loop...{Style.RESET_ALL}")
        
        self.current_loop = self.loop_manager.start_loop(
            self.player_id,
            self.cognitive_state,
            self.memory_bank
        )
        
        print(f"{Fore.GREEN}✓ Loop started{Style.RESET_ALL}")
        print(f"Loop Number: {Fore.YELLOW}{self.current_loop['loop_number']}{Style.RESET_ALL}")
        print(f"Duration: {Fore.YELLOW}{self.current_loop['duration_seconds']}s{Style.RESET_ALL}")
    
    async def generate_protocol(self):
        """Generate a protocol using LLM"""
        if not self.current_loop:
            print(f"{Fore.RED}✗ Please start a loop first{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Generating protocol with LLM...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏳ This may take 5-10 seconds...{Style.RESET_ALL}\n")
        
        difficulty = self.evolution_engine.calculate_protocol_difficulty(
            self.cognitive_state,
            "ethical_dilemma"
        )
        
        protocol = await self.llm_service.generate_ethical_dilemma(
            difficulty=difficulty,
            cognitive_focus=self.cognitive_state.dominant_traits,
            player_history={
                "dominant_traits": self.cognitive_state.dominant_traits,
                "evolution_score": self.cognitive_state.evolution_score
            }
        )
        
        print(f"{Fore.GREEN}✓ Protocol generated{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}{Style.BRIGHT}{protocol.get('title', 'Untitled')}{Style.RESET_ALL}")
        print(f"\n{protocol.get('scenario', 'No scenario')}\n")
        print(f"{Fore.YELLOW}Dilemma:{Style.RESET_ALL} {protocol.get('dilemma', 'No dilemma')}\n")
        
        if protocol.get('choices'):
            print(f"{Fore.YELLOW}Choices:{Style.RESET_ALL}")
            for i, choice in enumerate(protocol['choices'], 1):
                mentor = choice.get('mentor_alignment', 'UNKNOWN')
                print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {choice.get('text', 'No text')} "
                      f"({Fore.MAGENTA}{mentor}{Style.RESET_ALL})")
        
        return protocol
    
    def view_cognitive_state(self):
        """Display cognitive state"""
        if not self.cognitive_state:
            print(f"{Fore.RED}✗ Please initialize player first{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== COGNITIVE STATE ==={Style.RESET_ALL}")
        print(f"Evolution Score: {Fore.YELLOW}{self.cognitive_state.evolution_score:.1f}%{Style.RESET_ALL}")
        print(f"Loop Number: {Fore.YELLOW}{self.cognitive_state.loop_number}{Style.RESET_ALL}")
        print(f"Total XP: {Fore.YELLOW}{self.cognitive_state.total_experience}{Style.RESET_ALL}")
        
        if self.cognitive_state.dominant_traits:
            print(f"Dominant Traits: {Fore.YELLOW}{', '.join(self.cognitive_state.dominant_traits)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Modules:{Style.RESET_ALL}")
        for name, module in self.cognitive_state.modules.items():
            status_color = self._get_status_color(module.status.value)
            print(f"  {name.upper():12} | "
                  f"Level: {Fore.YELLOW}{module.level:5.1f}%{Style.RESET_ALL} | "
                  f"Status: {status_color}{module.status.value.upper()}{Style.RESET_ALL} | "
                  f"XP: {Fore.YELLOW}{module.experience_points}{Style.RESET_ALL}")
    
    def _get_status_color(self, status):
        """Get color for module status"""
        colors = {
            'locked': Fore.RED,
            'nascent': Fore.YELLOW,
            'developing': Fore.CYAN,
            'active': Fore.GREEN,
            'mastered': Fore.MAGENTA
        }
        return colors.get(status, Fore.WHITE)
    
    def view_evolution_tree(self):
        """Display evolution tree"""
        if not self.cognitive_state:
            print(f"{Fore.RED}✗ Please initialize player first{Style.RESET_ALL}")
            return
        
        tree_data = self.cognitive_state.get_neural_tree_data()
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== NEURAL EVOLUTION TREE ==={Style.RESET_ALL}")
        print(f"Evolution Score: {Fore.YELLOW}{tree_data['evolution_score']:.1f}%{Style.RESET_ALL}")
        print(f"Loop: {Fore.YELLOW}{tree_data['loop_number']}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Nodes:{Style.RESET_ALL}")
        for node in tree_data['nodes']:
            print(f"  {node['id']:12} | Level: {Fore.YELLOW}{node['level']:5.1f}%{Style.RESET_ALL} | "
                  f"Status: {node['status']}")
        
        print(f"\n{Fore.CYAN}Connections:{Style.RESET_ALL}")
        for link in tree_data['links']:
            print(f"  {link['source']:12} → {link['target']:12} | "
                  f"Strength: {Fore.YELLOW}{link['strength']:.2f}{Style.RESET_ALL}")
    
    def simulate_decision(self):
        """Simulate making a decision"""
        if not self.cognitive_state:
            print(f"{Fore.RED}✗ Please initialize player first{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Simulating decision...{Style.RESET_ALL}")
        
        # Sample decision impact
        impact = {
            "logic": 0.15,
            "empathy": 0.10,
            "creativity": 0.05
        }
        
        print(f"Decision impact: {impact}")
        
        self.cognitive_state = self.evolution_engine.apply_decision_impact(
            self.cognitive_state,
            impact,
            mentor_influence="LOGIC"
        )
        
        print(f"{Fore.GREEN}✓ Decision applied{Style.RESET_ALL}")
        print(f"New Evolution Score: {Fore.YELLOW}{self.cognitive_state.evolution_score:.1f}%{Style.RESET_ALL}")
        
        insights = self.evolution_engine.generate_evolution_insights(
            self.cognitive_state,
            []
        )
        
        if insights:
            print(f"\n{Fore.CYAN}Insights:{Style.RESET_ALL}")
            for insight in insights:
                print(f"  💡 {insight}")
    
    def complete_loop(self):
        """Complete current loop"""
        if not self.current_loop:
            print(f"{Fore.RED}✗ No active loop{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Completing loop...{Style.RESET_ALL}")
        
        result = self.loop_manager._complete_loop(self.current_loop['loop_id'])
        
        print(f"{Fore.GREEN}✓ Loop completed{Style.RESET_ALL}")
        print(f"Stats:")
        for key, value in result.get('stats', {}).items():
            print(f"  {key}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
        
        self.cognitive_state.loop_number += 1
        self.current_loop = None
    
    async def run_full_simulation(self):
        """Run a complete simulation"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}=== RUNNING FULL SIMULATION ==={Style.RESET_ALL}\n")
        
        # Initialize if needed
        if not self.cognitive_state:
            self.initialize_player()
            await asyncio.sleep(1)
        
        # Start loop
        self.start_loop()
        await asyncio.sleep(1)
        
        # Generate and process 3 protocols
        for i in range(3):
            print(f"\n{Fore.MAGENTA}--- Protocol {i+1}/3 ---{Style.RESET_ALL}")
            await self.generate_protocol()
            await asyncio.sleep(2)
            
            self.simulate_decision()
            await asyncio.sleep(1)
        
        # Complete loop
        self.complete_loop()
        await asyncio.sleep(1)
        
        # Show final state
        self.view_cognitive_state()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Simulation complete!{Style.RESET_ALL}\n")
    
    async def run(self):
        """Main demo loop"""
        self.print_header()
        
        while True:
            self.print_menu()
            
            try:
                choice = input(f"{Fore.CYAN}Select option: {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.initialize_player()
                elif choice == '2':
                    self.start_loop()
                elif choice == '3':
                    await self.generate_protocol()
                elif choice == '4':
                    self.view_cognitive_state()
                elif choice == '5':
                    self.view_evolution_tree()
                elif choice == '6':
                    self.simulate_decision()
                elif choice == '7':
                    self.complete_loop()
                elif choice == '8':
                    await self.run_full_simulation()
                elif choice == '9':
                    print(f"\n{Fore.CYAN}Thank you for testing PROTOCOL:LOOP!{Style.RESET_ALL}\n")
                    break
                else:
                    print(f"{Fore.RED}Invalid option{Style.RESET_ALL}")
                
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}Exiting demo...{Style.RESET_ALL}\n")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def main():
    """Run interactive demo"""
    demo = InteractiveDemo()
    asyncio.run(demo.run())


if __name__ == "__main__":
    main()