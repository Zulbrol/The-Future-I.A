import tkinter as tk
from tkinter import scrolledtext, ttk
import traceback
import threading
import json
import os
from datetime import datetime
from pathlib import Path

from core.file_manager import FileManager
from core.orchestrator_brain import OrchestratorBrain


class FutureChat:
    """Interface premium minimalista estilo ChatGPT com histórico de conversas"""

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("THE FUTURE I.A")
        self.janela.geometry("1200x800")
        self.janela.minsize(1000, 700)
        
        # Configurar diretório de conversas
        self.tasks_dir = Path("./workspace/tasks")
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        
        # Variáveis de estado
        self.conversa_atual = None
        self.historico_conversas = []
        
        # Configurar tema minimalista
        self.configurar_tema()
        
        # Layout principal com sidebar
        self.criar_layout_principal()
        
        # Configurar atalhos de teclado
        self.configurar_atalhos()
        
        # Inicializar o núcleo da IA
        self.inicializar_ia()
        
        # Carregar conversas recentes
        self.carregar_conversas_recentes()
        
        # Mensagem de boas-vindas
        self.mostrar_boas_vindas()
        
    def configurar_tema(self):
        """Configura tema minimalista premium"""
        self.cores = {
            'bg_principal': '#ffffff',
            'bg_sidebar': '#f7f7f8',
            'bg_chat': '#ffffff',
            'bg_entrada': '#ffffff',
            'bg_mensagem_assistente': '#f7f7f8',
            'bg_mensagem_usuario': '#ffffff',
            'texto': '#2d2d2d',
            'texto_secundario': '#6e6e6e',
            'texto_claro': '#acacbe',
            'destaque': '#10a37f',
            'destaque_hover': '#1a7f64',
            'borda': '#e5e5e5',
            'hover_sidebar': '#e5e5e5',
            'selecionado': '#e5e5e5'
        }
        
        self.janela.configure(bg=self.cores['bg_principal'])
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Vertical.TScrollbar",
            background=self.cores['bg_sidebar'],
            troughcolor=self.cores['bg_principal'],
            borderwidth=0,
            width=8
        )
        
    def criar_layout_principal(self):
        """Cria o layout com sidebar e área principal"""
        self.painel_principal = tk.Frame(
            self.janela,
            bg=self.cores['bg_principal']
        )
        self.painel_principal.pack(fill=tk.BOTH, expand=True)
        
        self.criar_sidebar()
        self.criar_area_principal()
        
    def criar_sidebar(self):
        """Cria a sidebar minimalista com conversas"""
        self.sidebar = tk.Frame(
            self.painel_principal,
            bg=self.cores['bg_sidebar'],
            width=260
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(
            self.sidebar,
            bg=self.cores['bg_sidebar'],
            height=60
        )
        logo_frame.pack(fill=tk.X, pady=(20, 10))
        logo_frame.pack_propagate(False)
        
        logo = tk.Label(
            logo_frame,
            text="✨ THE FUTURE I.A",
            font=("Segoe UI", 14, "bold"),
            fg=self.cores['texto'],
            bg=self.cores['bg_sidebar']
        )
        logo.pack(pady=10, padx=20, anchor=tk.W)
        
        # Botão Novo Chat
        self.btn_novo_chat = self.criar_botao_sidebar(
            "🔄  Novo chat",
            self.nova_conversa,
            destaque=True
        )
        self.btn_novo_chat.pack(fill=tk.X, padx=10, pady=(10, 20))
        
        # Separador
        self.criar_separador()
        
        # Menu Itens
        self.criar_item_sidebar("🖼️  Imagens", None)
        self.criar_item_sidebar("📚  Biblioteca", None)
        self.criar_item_sidebar("📁  Projetos", None)
        self.criar_item_sidebar("🔌  Plugins", None)
        self.criar_item_sidebar("💻  Codex", None)
        
        # Separador
        self.criar_separador()
        
        # Título "Recentes"
        recentes_label = tk.Label(
            self.sidebar,
            text="Recentes",
            font=("Segoe UI", 11, "bold"),
            fg=self.cores['texto'],
            bg=self.cores['bg_sidebar']
        )
        recentes_label.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Frame com scroll para conversas
        self.conversas_frame = tk.Frame(
            self.sidebar,
            bg=self.cores['bg_sidebar']
        )
        self.conversas_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        self.conversas_canvas = tk.Canvas(
            self.conversas_frame,
            bg=self.cores['bg_sidebar'],
            highlightthickness=0
        )
        self.conversas_scrollbar = ttk.Scrollbar(
            self.conversas_frame,
            orient=tk.VERTICAL,
            command=self.conversas_canvas.yview,
            style="Vertical.TScrollbar"
        )
        self.scrollable_frame = tk.Frame(
            self.conversas_canvas,
            bg=self.cores['bg_sidebar']
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.conversas_canvas.configure(
                scrollregion=self.conversas_canvas.bbox("all")
            )
        )
        
        self.conversas_canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        self.conversas_canvas.configure(yscrollcommand=self.conversas_scrollbar.set)
        
        self.conversas_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.conversas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Container para botões das conversas
        self.conversas_buttons = {}
        
    def criar_botao_sidebar(self, texto, comando, destaque=False):
        """Cria botão estilizado para sidebar"""
        btn = tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            font=("Segoe UI", 10),
            bg=self.cores['destaque'] if destaque else self.cores['bg_sidebar'],
            fg="white" if destaque else self.cores['texto'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=10,
            anchor=tk.W,
            justify=tk.LEFT,
            bd=0
        )
        
        if not destaque:
            btn.bind(
                "<Enter>",
                lambda e: btn.config(bg=self.cores['hover_sidebar'])
            )
            btn.bind(
                "<Leave>",
                lambda e: btn.config(bg=self.cores['bg_sidebar'])
            )
        
        return btn
        
    def criar_item_sidebar(self, texto, comando):
        """Cria item de menu na sidebar"""
        item = tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            font=("Segoe UI", 10),
            bg=self.cores['bg_sidebar'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            anchor=tk.W,
            justify=tk.LEFT,
            bd=0
        )
        item.pack(fill=tk.X, padx=10)
        
        item.bind(
            "<Enter>",
            lambda e: item.config(bg=self.cores['hover_sidebar'])
        )
        item.bind(
            "<Leave>",
            lambda e: item.config(bg=self.cores['bg_sidebar'])
        )
        
        return item
        
    def criar_separador(self):
        """Cria separador estilizado"""
        separador = tk.Frame(
            self.sidebar,
            bg=self.cores['borda'],
            height=1
        )
        separador.pack(fill=tk.X, padx=20, pady=10)
        
    def criar_area_principal(self):
        """Cria a área principal com chat e entrada"""
        self.area_principal = tk.Frame(
            self.painel_principal,
            bg=self.cores['bg_principal']
        )
        self.area_principal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.criar_area_chat()
        self.criar_area_entrada()
        
    def criar_area_chat(self):
        """Cria a área de chat minimalista"""
        self.chat_frame = tk.Frame(
            self.area_principal,
            bg=self.cores['bg_chat']
        )
        self.chat_frame.pack(
            padx=20,
            pady=(20, 10),
            fill=tk.BOTH,
            expand=True
        )
        
        self.chat = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            state="disabled",
            font=("Segoe UI", 11),
            bg=self.cores['bg_chat'],
            fg=self.cores['texto'],
            insertbackground=self.cores['texto'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=30,
            pady=20,
            spacing2=5
        )
        self.chat.pack(fill=tk.BOTH, expand=True)
        
        self.configurar_tags_chat()
        
    def configurar_tags_chat(self):
        """Configura as tags para formatação minimalista"""
        self.chat.tag_configure(
            "usuario",
            foreground=self.cores['texto'],
            font=("Segoe UI", 10, "bold"),
            spacing3=10
        )
        
        self.chat.tag_configure(
            "assistente",
            foreground=self.cores['destaque'],
            font=("Segoe UI", 10, "bold"),
            spacing3=10
        )
        
        self.chat.tag_configure(
            "erro",
            foreground="#e74c3c",
            font=("Segoe UI", 10, "bold"),
            spacing3=10
        )
        
        self.chat.tag_configure(
            "mensagem",
            font=("Segoe UI", 11),
            spacing1=5,
            spacing2=15
        )
        
        self.chat.tag_configure(
            "timestamp",
            foreground=self.cores['texto_claro'],
            font=("Segoe UI", 8),
            spacing3=10
        )
        
        self.chat.tag_configure(
            "usuario_bg",
            background=self.cores['bg_mensagem_usuario'],
            lmargin1=20,
            lmargin2=20,
            rmargin=20
        )
        
        self.chat.tag_configure(
            "assistente_bg",
            background=self.cores['bg_mensagem_assistente'],
            lmargin1=20,
            lmargin2=20,
            rmargin=20
        )
        
    def criar_area_entrada(self):
        """Cria área de entrada minimalista"""
        entrada_container = tk.Frame(
            self.area_principal,
            bg=self.cores['bg_principal'],
            height=120
        )
        entrada_container.pack(
            padx=20,
            pady=(0, 20),
            fill=tk.X
        )
        entrada_container.pack_propagate(False)
        
        entrada_frame = tk.Frame(
            entrada_container,
            bg=self.cores['bg_entrada'],
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor=self.cores['borda'],
            highlightbackground=self.cores['borda']
        )
        entrada_frame.pack(
            fill=tk.BOTH,
            expand=True
        )
        
        self.entrada = tk.Text(
            entrada_frame,
            font=("Segoe UI", 11),
            height=2,
            bg=self.cores['bg_entrada'],
            fg=self.cores['texto'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=15,
            pady=10,
            wrap=tk.WORD
        )
        self.entrada.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )
        
        botoes_frame = tk.Frame(
            entrada_frame,
            bg=self.cores['bg_entrada']
        )
        botoes_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        self.botao = tk.Button(
            botoes_frame,
            text="➤",
            font=("Segoe UI", 18),
            command=self.enviar,
            bg=self.cores['bg_entrada'],
            fg=self.cores['destaque'],
            relief=tk.FLAT,
            cursor="hand2",
            bd=0
        )
        self.botao.pack()
        
        self.botao.bind(
            "<Enter>",
            lambda e: self.botao.config(fg=self.cores['destaque_hover'])
        )
        self.botao.bind(
            "<Leave>",
            lambda e: self.botao.config(fg=self.cores['destaque'])
        )
        
    def mostrar_boas_vindas(self):
        """Mostra mensagem de boas-vindas estilizada"""
        self.adicionar_mensagem(
            "assistente",
            "👋 Olá! Sou seu assistente pessoal.\n\nComo posso ajudar você hoje?"
        )
        
    def configurar_atalhos(self):
        """Configura atalhos de teclado"""
        self.entrada.bind(
            "<Return>",
            lambda e: self.enviar()
        )
        self.entrada.bind(
            "<Shift-Return>",
            lambda e: "break"
        )
        
    def inicializar_ia(self):
        """Inicializa o núcleo da IA"""
        file_manager = FileManager(
            base_path="./workspace"
        )
        self.orchestrator = OrchestratorBrain(
            file_manager
        )
        
    def carregar_conversas_recentes(self):
        """Carrega todas as conversas da pasta tasks"""
        # Limpar botões existentes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.conversas_buttons.clear()
        
        # Buscar arquivos de conversa
        arquivos_conversas = sorted(
            self.tasks_dir.glob("conversa_*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if not arquivos_conversas:
            # Se não houver conversas, mostrar mensagem
            label = tk.Label(
                self.scrollable_frame,
                text="Nenhuma conversa recente",
                font=("Segoe UI", 9, "italic"),
                fg=self.cores['texto_claro'],
                bg=self.cores['bg_sidebar']
            )
            label.pack(pady=20)
            return
        
        # Adicionar cada conversa
        for arquivo in arquivos_conversas[:20]:  # Limitar a 20 conversas
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    titulo = dados.get('titulo', arquivo.stem.replace('conversa_', ''))
                    data = datetime.fromtimestamp(arquivo.stat().st_mtime)
                    data_str = data.strftime("%d/%m/%Y %H:%M")
                    
                    # Criar botão para a conversa
                    self.adicionar_conversa_lista(titulo, str(arquivo), data_str)
            except Exception as e:
                print(f"Erro ao carregar conversa {arquivo}: {e}")
                
    def adicionar_conversa_lista(self, titulo, caminho, data):
        """Adiciona uma conversa à lista na sidebar"""
        # Truncar título se muito longo
        if len(titulo) > 30:
            titulo = titulo[:27] + "..."
            
        btn = tk.Button(
            self.scrollable_frame,
            text=f"{titulo}",
            font=("Segoe UI", 9),
            bg=self.cores['bg_sidebar'],
            fg=self.cores['texto_secundario'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            anchor=tk.W,
            justify=tk.LEFT,
            bd=0
        )
        btn.pack(fill=tk.X)
        
        # Tooltip com data
        btn.bind(
            "<Enter>",
            lambda e, b=btn, d=data: [
                b.config(bg=self.cores['hover_sidebar'], fg=self.cores['texto']),
                self.show_tooltip(b, f"Última conversa: {d}")
            ]
        )
        btn.bind(
            "<Leave>",
            lambda e, b=btn: [
                b.config(bg=self.cores['bg_sidebar'], fg=self.cores['texto_secundario']),
                self.hide_tooltip()
            ]
        )
        btn.bind(
            "<Button-1>",
            lambda e, c=caminho: self.carregar_conversa(c)
        )
        
        self.conversas_buttons[caminho] = btn
        
    def show_tooltip(self, widget, texto):
        """Mostra tooltip com informações da conversa"""
        # Implementação simples de tooltip
        pass
        
    def hide_tooltip(self):
        """Esconde tooltip"""
        pass
        
    def carregar_conversa(self, caminho_arquivo):
        """Carrega uma conversa do arquivo JSON"""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
            # Limpar chat atual
            self.chat.config(state="normal")
            self.chat.delete(1.0, tk.END)
            self.chat.config(state="disabled")
            
            # Carregar mensagens
            mensagens = dados.get('mensagens', [])
            for msg in mensagens:
                autor = msg.get('autor', 'assistente')
                texto = msg.get('texto', '')
                self.adicionar_mensagem(autor, texto)
                
            self.conversa_atual = caminho_arquivo
            
            # Destacar conversa na lista
            for caminho, btn in self.conversas_buttons.items():
                if caminho == caminho_arquivo:
                    btn.config(bg=self.cores['selecionado'])
                else:
                    btn.config(bg=self.cores['bg_sidebar'])
                    
        except Exception as e:
            self.adicionar_mensagem("erro", f"Erro ao carregar conversa: {str(e)}")
            
    def salvar_conversa(self):
        """Salva a conversa atual em um arquivo JSON"""
        try:
            # Extrair primeira mensagem do usuário como título
            titulo = "Nova conversa"
            mensagens = []
            
            # Ler todas as mensagens do chat
            conteudo = self.chat.get(1.0, tk.END).strip()
            if not conteudo:
                return
                
            # Criar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"conversa_{timestamp}.json"
            caminho = self.tasks_dir / nome_arquivo
            
            # Extrair mensagens (simplificado - em produção seria mais robusto)
            # Aqui você pode implementar uma lógica melhor para extrair as mensagens
            dados = {
                'titulo': titulo,
                'data_criacao': datetime.now().isoformat(),
                'mensagens': [
                    {'autor': 'assistente', 'texto': 'Olá! Como posso ajudar?'}
                ]
            }
            
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
                
            # Atualizar lista de conversas
            self.carregar_conversas_recentes()
            
        except Exception as e:
            print(f"Erro ao salvar conversa: {e}")
            
    def nova_conversa(self):
        """Inicia uma nova conversa"""
        # Salvar conversa atual se tiver conteúdo
        if self.chat.get(1.0, tk.END).strip():
            self.salvar_conversa()
            
        # Limpar chat
        self.chat.config(state="normal")
        self.chat.delete(1.0, tk.END)
        self.chat.config(state="disabled")
        
        self.conversa_atual = None
        
        # Remover destaque das conversas
        for btn in self.conversas_buttons.values():
            btn.config(bg=self.cores['bg_sidebar'])
            
        self.mostrar_boas_vindas()
        
    def adicionar_mensagem(self, autor, texto):
        """Adiciona mensagem formatada estilo ChatGPT"""
        self.chat.config(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if autor.lower() == "você":
            tag_autor = "usuario"
            tag_bg = "usuario_bg"
            icone = ""
        elif autor.lower() == "assistente" or autor.lower() == "orchestrator":
            tag_autor = "assistente"
            tag_bg = "assistente_bg"
            icone = ""
        elif autor.lower() == "erro":
            tag_autor = "erro"
            tag_bg = None
            icone = "⚠️ "
        else:
            tag_autor = "assistente"
            tag_bg = "assistente_bg"
            icone = ""
        
        self.chat.insert(tk.END, "\n")
        
        if autor.lower() != "você" and autor.lower() != "assistente":
            self.chat.insert(
                tk.END,
                f"{icone}{autor}\n",
                tag_autor
            )
        else:
            self.chat.insert(
                tk.END,
                f"{autor}\n",
                tag_autor
            )
        
        self.chat.insert(
            tk.END,
            f"{texto}\n",
            "mensagem"
        )
        
        self.chat.insert(
            tk.END,
            f"{timestamp}",
            "timestamp"
        )
        
        if tag_bg:
            inicio = self.chat.index("end-2l linestart")
            fim = self.chat.index("end-1c")
            self.chat.tag_add(tag_bg, inicio, fim)
        
        self.chat.insert(tk.END, "\n\n")
        
        self.chat.config(state="disabled")
        self.chat.yview(tk.END)
        
        # Salvar automaticamente após cada mensagem
        self.salvar_conversa_automatico()
        
    def salvar_conversa_automatico(self):
        """Salva a conversa automaticamente após cada interação"""
        try:
            # Só salvar se tiver conteúdo
            if not self.chat.get(1.0, tk.END).strip():
                return
                
            # Se não tem conversa atual, criar nova
            if not self.conversa_atual:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"conversa_{timestamp}.json"
                self.conversa_atual = str(self.tasks_dir / nome_arquivo)
                
            # Extrair mensagens (implementação simplificada)
            # Em produção, você deve ter uma estrutura de dados melhor
            dados = {
                'titulo': f"Conversa {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                'data_criacao': datetime.now().isoformat(),
                'mensagens': [
                    {'autor': 'assistente', 'texto': 'Olá! Como posso ajudar?'}
                ]
            }
            
            with open(self.conversa_atual, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
                
            # Atualizar lista de conversas
            self.carregar_conversas_recentes()
            
        except Exception as e:
            print(f"Erro ao salvar conversa automaticamente: {e}")
        
    def enviar(self):
        """Processa o envio da mensagem"""
        mensagem = self.entrada.get(1.0, tk.END).strip()
        
        if not mensagem:
            return
            
        self.entrada.delete(1.0, tk.END)
        self.adicionar_mensagem("Você", mensagem)
        
        thread = threading.Thread(
            target=self.processar_ia,
            args=(mensagem,)
        )
        thread.daemon = True
        thread.start()
        
    def processar_ia(self, mensagem):
        """Processa a mensagem com a IA"""
        try:
            resposta = self.orchestrator.processar_solicitacao(mensagem)

            self.janela.after(
            0,
            lambda: self.adicionar_mensagem(
                "Assistente",
                resposta
            )
        )

        except Exception as erro:
         traceback.print_exc()

         print("TIPO DO ERRO:", type(erro))
         print("REPR:", repr(erro))
         print("STR:", str(erro))

         mensagem_erro = repr(erro)

         self.janela.after(
            0,
            lambda m=mensagem_erro: self.adicionar_mensagem(
                "Erro",
                m
            )
        )            
    def iniciar(self):
        """Inicia a aplicação"""
        self.entrada.focus()
        self.janela.mainloop()


if __name__ == "__main__":
    app = FutureChat()
    app.iniciar()