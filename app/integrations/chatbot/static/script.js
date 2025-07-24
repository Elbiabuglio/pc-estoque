/**
 * PC-Estoque Chatbot - Professional Interface JavaScript
 * Advanced interactive features and modern UX
 */

// === FUNÇÕES GLOBAIS SIMPLES (DEFINIDAS PRIMEIRO) ===

// Função de TESTE para debug
window.testModal = function() {
    console.log('🧪 TESTE DIRETO DO MODAL');
    const modal = document.getElementById('sellerIdModal');
    const input = document.getElementById('sellerIdInput');
    
    console.log('Modal encontrado:', modal);
    console.log('Input encontrado:', input);
    
    if (modal) {
        modal.style.display = 'flex';
        modal.style.zIndex = '10000';
        console.log('✅ Modal forçado a aparecer');
        
        if (input) {
            input.focus();
            console.log('✅ Input focado');
        }
    } else {
        console.error('❌ Modal não encontrado no DOM!');
    }
};

// Função de TESTE para simular identificação diretamente
window.testIdentification = function(sellerId = 'seller123') {
    console.log('🧪 TESTE DIRETO DE IDENTIFICAÇÃO:', sellerId);
    
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.value = `identificar ${sellerId}`;
        console.log('✅ Comando definido:', messageInput.value);
        
        // Tentar via chatInterface
        if (window.chatInterface && window.chatInterface.sendMessage) {
            console.log('📤 Enviando via chatInterface...');
            window.chatInterface.sendMessage();
        } else {
            console.log('📤 Enviando via botão...');
            const sendBtn = document.getElementById('sendButton');
            if (sendBtn) {
                sendBtn.click();
            }
        }
    }
};

// Função SUPER SIMPLES para teste
window.testSimple = function() {
    console.log('🔥 TESTE SUPER SIMPLES INICIADO');
    
    // Verificar elementos básicos
    console.log('🔍 Verificando elementos:');
    console.log('  - messageInput:', !!document.getElementById('messageInput'));
    console.log('  - sendButton:', !!document.getElementById('sendButton'));
    console.log('  - chatInterface:', !!window.chatInterface);
    
    // Tentar enviar mensagem simples
    const input = document.getElementById('messageInput');
    const button = document.getElementById('sendButton');
    
    if (input && button) {
        input.value = 'identificar teste123';
        console.log('✅ Valor inserido:', input.value);
        
        // Simular clique no botão
        console.log('🖱️ Clicando no botão...');
        button.click();
        
        // Verificar se funcionou
        setTimeout(() => {
            console.log('🔍 Após 1s - Input value:', input.value);
            console.log('🔍 Após 1s - Chat messages:', document.getElementById('chatMessages').children.length);
        }, 1000);
    } else {
        console.error('❌ Elementos não encontrados!');
    }
};

// Função PRINCIPAL para abrir o modal
window.promptSellerId = function() {
    console.log('🚀 FUNÇÃO PRINCIPAL promptSellerId chamada!');
    
    // Chamar função de teste primeiro
    window.testModal();
};

// Função PRINCIPAL para confirmar
window.confirmSellerId = function() {
    console.log('🚀 FUNÇÃO PRINCIPAL confirmSellerId chamada!');
    
    const input = document.getElementById('sellerIdInput');
    const messageInput = document.getElementById('messageInput');
    const modal = document.getElementById('sellerIdModal');
    const sendBtn = document.getElementById('sendButton');
    
    console.log('Input modal encontrado:', !!input);
    console.log('Input mensagem encontrado:', !!messageInput);
    console.log('Botão enviar encontrado:', !!sendBtn);
    
    if (!input) {
        console.error('❌ Input do modal não encontrado!');
        return;
    }
    
    const sellerId = input.value.trim();
    console.log('Seller ID digitado:', sellerId);
    
    if (!sellerId) {
        alert('Por favor, digite seu seller_id');
        input.focus();
        return;
    }
    
    // Fechar modal primeiro
    if (modal) {
        modal.style.display = 'none';
        input.value = '';
    }
    
    // Definir comando no input principal
    if (messageInput) {
        messageInput.value = `identificar ${sellerId}`;
        console.log('✅ Comando inserido no input principal:', messageInput.value);
    }
    
    // FORÇAR o envio de múltiplas formas
    console.log('📤 Tentando enviar mensagem...');
    
    // Tentar via botão primeiro
    if (sendBtn) {
        console.log('🎯 Tentativa 1: Clicando no botão enviar');
        sendBtn.click();
    }
    
    // Tentar via chatInterface se disponível
    setTimeout(() => {
        if (window.chatInterface && window.chatInterface.sendMessage) {
            console.log('🎯 Tentativa 2: Via chatInterface.sendMessage');
            window.chatInterface.sendMessage();
        }
    }, 100);
    
    // Último recurso: envio direto via API
    setTimeout(() => {
        if (messageInput && messageInput.value.trim()) {
            console.log('🎯 Tentativa 3: Envio direto via API');
            const message = messageInput.value.trim();
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    mensagem: message,
                    session_id: window.chatInterface ? window.chatInterface.sessionId : 'fallback_session'
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('✅ Resposta da API recebida:', data);
                
                // Limpar input
                messageInput.value = '';
                
                // Adicionar mensagem do usuário manualmente
                const chatMessages = document.getElementById('chatMessages');
                if (chatMessages) {
                    const userMsg = document.createElement('div');
                    userMsg.className = 'message-container user';
                    userMsg.innerHTML = `
                        <div class="message-bubble">${message}</div>
                        <div class="message-time">${new Date().toLocaleTimeString('pt-BR')}</div>
                    `;
                    chatMessages.appendChild(userMsg);
                    
                    // Adicionar resposta do bot
                    const botMsg = document.createElement('div');
                    botMsg.className = 'message-container bot';
                    botMsg.innerHTML = `
                        <div class="message-bubble">${data.resposta.replace(/\n/g, '<br>')}</div>
                        <div class="message-time">${new Date().toLocaleTimeString('pt-BR')}</div>
                    `;
                    chatMessages.appendChild(botMsg);
                    
                    // Scroll para baixo
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    
                    console.log('✅ Mensagens adicionadas ao chat');
                }
            })
            .catch(error => {
                console.error('❌ Erro no envio direto:', error);
            });
        }
    }, 300);
    
    // Esconder alert de identificação
    const alert = document.getElementById('identificationAlert');
    if (alert) {
        alert.classList.add('hidden');
    }
    localStorage.setItem('userIdentified', 'true');
};

// Função PRINCIPAL para fechar modal
window.closeSellerIdModal = function() {
    console.log('🚀 FUNÇÃO PRINCIPAL closeSellerIdModal chamada!');
    
    const modal = document.getElementById('sellerIdModal');
    const input = document.getElementById('sellerIdInput');
    
    if (modal) {
        modal.style.display = 'none';
        console.log('✅ Modal fechado');
    }
    
    if (input) {
        input.value = '';
        console.log('✅ Input limpo');
    }
};

// === CLASSE PRINCIPAL ===

class ChatInterface {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isLoading = false;
        this.messageCount = 0;
        this.theme = localStorage.getItem('theme') || 'auto';
        this.sidebarOpen = false;
        this.notifications = [];
        this.autocompleteData = this.initializeAutocomplete();
        this.fabMenuOpen = false;
        this.initializeInterface();
        this.setupEventListeners();
        this.checkSystemStatus();
        this.applyTheme();
        this.initializeAnalytics();
        this.setupVoiceRecognition();
    }

    /**
     * Gera um ID único para a sessão do usuário
     */
    generateSessionId() {
        return 'web_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Inicializa a interface do chat
     */
    initializeInterface() {
        // Elementos principais
        this.messagesContainer = document.getElementById('chatMessages');
        this.loadingElement = document.getElementById('loading');
        this.inputElement = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.charCounter = document.getElementById('charCount');
        this.sidebar = document.getElementById('sidebar');
        this.quickCommands = document.getElementById('quickCommands');

        // Auto-resize textarea
        this.setupAutoResize();

        // Focar no input
        this.focusInput();

        console.log('🤖 Interface profissional carregada');
        console.log('Session ID:', this.sessionId);
    }

    /**
     * Configura redimensionamento automático do textarea
     */
    setupAutoResize() {
        if (this.inputElement) {
            this.inputElement.addEventListener('input', () => {
                this.inputElement.style.height = 'auto';
                this.inputElement.style.height = Math.min(this.inputElement.scrollHeight, 120) + 'px';
                this.updateCharacterCount();
            });
        }
    }

    /**
     * Configura os listeners de eventos
     */
    setupEventListeners() {
        // Enter para enviar (Ctrl+Enter para nova linha)
        if (this.inputElement) {
            this.inputElement.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        // Botão de envio
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => {
                this.sendMessage();
            });
        }

        // Menu mobile
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Toggle sidebar
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }

        // Verificar status periodicamente
        this.statusInterval = setInterval(() => {
            this.checkSystemStatus();
        }, 30000);

        // Eventos de conectividade
        window.addEventListener('online', () => {
            this.showToast('Conexão reestabelecida', 'success');
            this.checkSystemStatus();
        });

        window.addEventListener('offline', () => {
            this.showToast('Conexão perdida', 'warning');
        });

        // Cleanup
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });

        // Clique fora para fechar menus
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.quick-commands') && 
                !e.target.closest('[onclick*="toggleCommands"]')) {
                this.hideQuickCommands();
            }
        });
    }

    /**
     * Aplica tema (claro/escuro/auto)
     */
    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        
        // Atualizar ícone do botão de tema
        const themeBtn = document.querySelector('[onclick="toggleTheme()"] i');
        if (themeBtn) {
            const isDark = this.theme === 'dark' || 
                (this.theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
            themeBtn.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    /**
     * Alterna tema
     */
    toggleTheme() {
        const themes = ['auto', 'light', 'dark'];
        const currentIndex = themes.indexOf(this.theme);
        this.theme = themes[(currentIndex + 1) % themes.length];
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
        
        const themeNames = { auto: 'Automático', light: 'Claro', dark: 'Escuro' };
        this.showToast(`Tema alterado para ${themeNames[this.theme]}`, 'success');
    }

    /**
     * Toggle sidebar em mobile
     */
    toggleSidebar() {
        this.sidebarOpen = !this.sidebarOpen;
        if (this.sidebar) {
            this.sidebar.classList.toggle('open', this.sidebarOpen);
        }
    }

    /**
     * Envia uma mensagem para o chatbot
     */
    async sendMessage() {
        const message = this.inputElement.value.trim();
        
        console.log('📤 sendMessage chamado com:', message);
        console.log('🔍 isLoading:', this.isLoading);
        
        if (!message || this.isLoading) {
            console.log('❌ Mensagem vazia ou loading ativo');
            return;
        }

        // Validações
        if (message.length > 500) {
            this.showToast('Mensagem muito longa. Máximo 500 caracteres.', 'error');
            return;
        }

        try {
            console.log('✅ Iniciando envio da mensagem:', message);
            
            // Limpar input e mostrar loading
            this.inputElement.value = '';
            this.inputElement.style.height = 'auto';
            this.updateCharacterCount();
            this.setLoading(true);

            // Adicionar mensagem do usuário
            console.log('📝 Adicionando mensagem do usuário ao chat');
            this.addMessage(message, 'user');

            // Enviar para API
            console.log('🌐 Enviando para API...');
            const response = await this.callChatAPI(message);
            console.log('✅ Resposta da API recebida:', response);
            
            // Adicionar resposta do bot
            console.log('🤖 Adicionando resposta do bot ao chat');
            this.addMessage(response.resposta, 'bot');

            // Log da interação
            this.logInteraction(message, response.resposta);

        } catch (error) {
            console.error('❌ Erro ao enviar mensagem:', error);
            this.handleError(error);
        } finally {
            this.setLoading(false);
            this.focusInput();
        }
    }

    /**
     * Chama a API do chatbot
     */
    async callChatAPI(message) {
        const requestData = {
            mensagem: message,
            session_id: this.sessionId,
            timestamp: new Date().toISOString(),
            source: 'web_interface_pro'
        };

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(requestData),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Erro ${response.status}: ${errorText}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Adiciona uma mensagem ao chat
     */
    addMessage(content, sender, timestamp = null) {
        if (!this.messagesContainer) return;

        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${sender}`;
        messageContainer.setAttribute('data-message-id', ++this.messageCount);

        const messageBubble = document.createElement('div');
        messageBubble.className = 'message-bubble';
        
        // Processar conteúdo
        messageBubble.innerHTML = this.processMessageContent(content);

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = timestamp || new Date().toLocaleTimeString('pt-BR');

        messageContainer.appendChild(messageBubble);
        messageContainer.appendChild(timeDiv);
        this.messagesContainer.appendChild(messageContainer);

        // Scroll suave
        this.scrollToBottom();
    }

    /**
     * Processa o conteúdo da mensagem
     */
    processMessageContent(content) {
        // Verificar se é uma mensagem de acesso autorizado
        if (content.startsWith('ACESSO_AUTORIZADO:')) {
            return this.renderAccessGrantedMessage(content);
        }
        
        // Escapar HTML e processar apenas quebras de linha
        const div = document.createElement('div');
        div.textContent = content;
        let processedContent = div.innerHTML;

        // Processar apenas quebras de linha
        processedContent = processedContent.replace(/\n/g, '<br>');

        return processedContent;
    }

    /**
     * Renderiza mensagem especial de acesso autorizado
     */
    renderAccessGrantedMessage(content) {
        // Extrair dados da mensagem
        const lines = content.split('\n');
        const userIdMatch = lines[0].match(/ACESSO_AUTORIZADO:(.+)/);
        const userId = userIdMatch ? userIdMatch[1] : 'Usuário';
        
        // Extrair comandos das linhas
        const comandos = {
            gestao: [],
            sistema: []
        };
        
        let currentSection = '';
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.includes('📦 GESTÃO DE ESTOQUE')) {
                currentSection = 'gestao';
            } else if (line.includes('⚙️ SISTEMA & RELATÓRIOS')) {
                currentSection = 'sistema';
            } else if (line.startsWith('•') && currentSection) {
                comandos[currentSection].push(line.substring(1).trim());
            }
        }

        return `
            <div class="access-granted-message">
                <div class="access-header">
                    <div class="access-icon">🎉</div>
                    <div class="access-title">ACESSO AUTORIZADO</div>
                    <div class="access-subtitle">Bem-vindo ao PC-Estoque, <strong>${userId}</strong>!</div>
                </div>
                
                <div class="access-description">
                    Você agora tem acesso completo ao sistema de controle inteligente de estoque.
                </div>
                
                <div class="commands-grid">
                    <div class="command-section">
                        <div class="section-header">
                            <span class="section-icon">📦</span>
                            <span class="section-title">Gestão de Estoque</span>
                        </div>
                        <div class="command-list">
                            ${comandos.gestao.map(cmd => `
                                <div class="command-item" onclick="insertQuickCommand('${cmd.split(' - ')[0].split(' ')[0]}')">
                                    <div class="command-name">${cmd.split(' - ')[0]}</div>
                                    <div class="command-desc">${cmd.split(' - ')[1] || ''}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="command-section">
                        <div class="section-header">
                            <span class="section-icon">⚙️</span>
                            <span class="section-title">Sistema & Relatórios</span>
                        </div>
                        <div class="command-list">
                            ${comandos.sistema.map(cmd => `
                                <div class="command-item" onclick="insertQuickCommand('${cmd.split(' - ')[0].split(' ')[0]}')">
                                    <div class="command-name">${cmd.split(' - ')[0]}</div>
                                    <div class="command-desc">${cmd.split(' - ')[1] || ''}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                
                <div class="access-tip">
                    <span class="tip-icon">💡</span>
                    <span class="tip-text">Clique em qualquer comando acima para começar, ou digite diretamente no campo de mensagem!</span>
                </div>
            </div>
        `;
    }

    /**
     * Controla o estado de loading
     */
    setLoading(loading) {
        this.isLoading = loading;

        if (this.loadingElement) {
            this.loadingElement.classList.toggle('show', loading);
        }

        if (this.sendButton) {
            this.sendButton.disabled = loading;
            const icon = this.sendButton.querySelector('i');
            if (icon) {
                icon.className = loading ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane';
            }
        }

        if (this.inputElement) {
            this.inputElement.disabled = loading;
        }

        if (loading) {
            this.scrollToBottom();
        }
    }

    /**
     * Foca no input de mensagem
     */
    focusInput() {
        if (this.inputElement && !this.inputElement.disabled) {
            this.inputElement.focus();
        }
    }

    /**
     * Scroll suave para o final
     */
    scrollToBottom() {
        if (this.messagesContainer) {
            setTimeout(() => {
                this.messagesContainer.scrollTo({
                    top: this.messagesContainer.scrollHeight,
                    behavior: 'smooth'
                });
            }, 100);
        }
    }

    /**
     * Verifica status do sistema
     */
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/status', {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                const status = await response.json();
                this.updateStatusIndicator(status);
            } else {
                throw new Error('Falha ao verificar status');
            }
        } catch (error) {
            console.error('Erro ao verificar status:', error);
            this.updateStatusIndicator({ 
                status: 'error', 
                chatbot_disponivel: false 
            });
        }
    }

    /**
     * Atualiza indicador de status
     */
    updateStatusIndicator(status) {
        const indicators = document.querySelectorAll('.status-indicator');
        indicators.forEach(indicator => {
            const isOnline = status.chatbot_disponivel;
            indicator.className = `status-indicator ${isOnline ? 'online' : 'offline'}`;
        });

        // Atualizar texto de status
        const statusInfo = document.querySelector('.status-info');
        if (statusInfo) {
            const h3 = statusInfo.querySelector('h3');
            const p = statusInfo.querySelector('p');
            if (h3 && p) {
                h3.textContent = `Sistema ${status.chatbot_disponivel ? 'Online' : 'Offline'}`;
                p.textContent = status.chatbot_disponivel ? 
                    'IA e Banco Integrados' : 'Modo Limitado';
            }
        }
    }

    /**
     * Mostra toast notification
     */
    showToast(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        }[type] || 'fas fa-info-circle';

        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;

        container.appendChild(toast);

        // Auto-remove
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, duration);
    }

    /**
     * Trata erros
     */
    handleError(error) {
        let errorMessage = 'Erro inesperado. Tente novamente.';

        if (error.name === 'AbortError') {
            errorMessage = 'Tempo limite excedido. Tente uma mensagem mais simples.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Erro de conexão. Verifique sua internet.';
        } else if (error.message.includes('500')) {
            errorMessage = 'Erro interno do servidor. Tente novamente em instantes.';
        } else if (error.message.includes('400')) {
            errorMessage = 'Formato de mensagem inválido. Tente reformular.';
        }

        this.addMessage(`❌ ${errorMessage}`, 'bot');
        this.showToast(errorMessage, 'error');
    }

    /**
     * Atualiza contador de caracteres
     */
    updateCharacterCount() {
        if (!this.inputElement || !this.charCounter) return;

        const length = this.inputElement.value.length;
        this.charCounter.textContent = length;
        
        // Cor baseada no uso
        if (length > 400) {
            this.charCounter.style.color = '#dc3545';
        } else if (length > 300) {
            this.charCounter.style.color = '#ffc107';
        } else {
            this.charCounter.style.color = '#6c757d';
        }
    }

    /**
     * Mostra/esconde comandos rápidos
     */
    toggleQuickCommands() {
        if (this.quickCommands) {
            this.quickCommands.classList.toggle('show');
        }
    }

    /**
     * Esconde comandos rápidos
     */
    hideQuickCommands() {
        if (this.quickCommands) {
            this.quickCommands.classList.remove('show');
        }
    }

    /**
     * Insere comando no input
     */
    insertCommand(command) {
        if (this.inputElement) {
            // Tratamento especial para o comando identificar
            if (command.includes('/identificar ')) {
                this.promptSellerId();
                return;
            }
            
            this.inputElement.value = command;
            this.inputElement.focus();
            this.inputElement.setSelectionRange(command.length, command.length);
            this.updateCharacterCount();
        }
        this.hideQuickCommands();
    }

    /**
     * Prompt específico para solicitar seller_id
     */
    promptSellerId() {
        console.log('🎯 promptSellerId método da classe chamado');
        
        // Mostrar modal customizado
        const modal = document.getElementById('sellerIdModal');
        const input = document.getElementById('sellerIdInput');
        
        console.log('📋 Modal encontrado:', !!modal);
        console.log('📝 Input encontrado:', !!input);
        
        if (modal) {
            modal.style.display = 'flex';
            console.log('✅ Modal exibido com display flex');
            
            // Focar no input após um pequeno delay
            setTimeout(() => {
                if (input) {
                    input.focus();
                    input.select(); // Selecionar qualquer texto existente
                    console.log('✅ Input focado e selecionado');
                }
            }, 150);
        } else {
            console.error('❌ Modal sellerIdModal não encontrado no DOM!');
            // Fallback: usar prompt nativo
            const sellerId = prompt('Digite seu Seller ID:');
            if (sellerId && sellerId.trim()) {
                this.inputElement.value = `identificar ${sellerId.trim()}`;
                this.sendMessage();
            }
            return;
        }
        
        // Configurar listener para Enter no input (remover listeners antigos primeiro)
        if (input) {
            // Remover listeners antigos
            input.removeEventListener('keypress', this.sellerIdEnterHandler);
            
            // Criar novo handler
            this.sellerIdEnterHandler = (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.confirmSellerId();
                }
            };
            
            // Adicionar novo listener
            input.addEventListener('keypress', this.sellerIdEnterHandler);
            console.log('✅ Event listener configurado para Enter');
        }
    }

    /**
     * Confirma o seller_id inserido
     */
    confirmSellerId() {
        console.log('🔧 confirmSellerId chamado');
        const input = document.getElementById('sellerIdInput');
        
        if (!input) {
            console.error('❌ Input sellerIdInput não encontrado!');
            return;
        }
        
        const sellerId = input.value.trim();
        console.log('📝 Seller ID digitado:', sellerId);
        
        if (sellerId) {
            const command = `identificar ${sellerId}`;
            console.log('💬 Comando a ser enviado:', command);
            
            // Definir o comando no input principal
            if (this.inputElement) {
                this.inputElement.value = command;
                console.log('✅ Comando inserido no input principal');
            }
            
            // Fechar modal ANTES de enviar
            this.closeSellerIdModal();
            
            // Esconder o alert de identificação
            const alert = document.getElementById('identificationAlert');
            if (alert) {
                alert.classList.add('hidden');
                console.log('✅ Alert de identificação escondido');
            }
            
            // Marcar que o usuário se identificou
            localStorage.setItem('userIdentified', 'true');
            
            // FORÇAR envio da mensagem com pequeno delay
            console.log('📤 Enviando mensagem...');
            setTimeout(() => {
                // Tentar múltiplas formas de envio
                console.log('🚀 Tentativa 1: Método sendMessage direto');
                this.sendMessage();
                
                // Se não funcionou, tentar clicar no botão
                setTimeout(() => {
                    const sendBtn = document.getElementById('sendButton');
                    if (sendBtn && this.inputElement && this.inputElement.value.trim()) {
                        console.log('🚀 Tentativa 2: Clique no botão send');
                        sendBtn.click();
                    }
                    
                    // Se ainda não funcionou, simular Enter
                    setTimeout(() => {
                        if (this.inputElement && this.inputElement.value.trim()) {
                            console.log('🚀 Tentativa 3: Simular Enter');
                            const enterEvent = new KeyboardEvent('keydown', {
                                key: 'Enter',
                                code: 'Enter',
                                keyCode: 13,
                                which: 13,
                                bubbles: true
                            });
                            this.inputElement.dispatchEvent(enterEvent);
                        }
                    }, 100);
                }, 100);
            }, 100);
            
        } else {
            console.log('⚠️ Seller ID vazio');
            this.showToast("⚠️ Por favor, digite seu seller_id", "warning");
            input.focus();
        }
    }

    /**
     * Fecha o modal de seller_id
     */
    closeSellerIdModal() {
        console.log('🔒 Fechando modal de seller ID');
        const modal = document.getElementById('sellerIdModal');
        const input = document.getElementById('sellerIdInput');
        
        if (modal) {
            modal.style.display = 'none';
            console.log('✅ Modal escondido');
        }
        
        if (input) {
            input.value = '';
            // Remover event listener se existir
            if (this.sellerIdEnterHandler) {
                input.removeEventListener('keypress', this.sellerIdEnterHandler);
            }
            console.log('✅ Input limpo e listener removido');
        }
    }

    /**
     * Exporta histórico
     */
    exportChatHistory() {
        const messages = Array.from(this.messagesContainer.querySelectorAll('.message-container'));
        const history = messages.map(msg => {
            const content = msg.querySelector('.message-bubble').textContent;
            const time = msg.querySelector('.message-time').textContent;
            const sender = msg.classList.contains('user') ? 'Usuário' : 'Bot';
            return `[${time}] ${sender}: ${content}`;
        }).join('\n');

        const blob = new Blob([history], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pc-estoque-chat-${new Date().toISOString().split('T')[0]}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showToast('Histórico exportado com sucesso!', 'success');
    }

    /**
     * Limpa histórico
     */
    clearChatHistory() {
        if (confirm('Tem certeza que deseja limpar o histórico do chat?')) {
            const messages = this.messagesContainer.querySelectorAll('.message-container');
            messages.forEach(msg => {
                if (!msg.classList.contains('welcome-container')) {
                    msg.remove();
                }
            });
            this.messageCount = 0;
            this.showToast('Histórico limpo', 'success');
        }
    }

    /**
     * Log de interação
     */
    logInteraction(userMessage, botResponse) {
        console.log('📊 Interação registrada:', {
            session: this.sessionId,
            timestamp: new Date().toISOString(),
            user: userMessage.substring(0, 50) + (userMessage.length > 50 ? '...' : ''),
            bot: botResponse.substring(0, 50) + (botResponse.length > 50 ? '...' : ''),
            messageCount: this.messageCount
        });
    }

    /**
     * Limpa recursos
     */
    cleanup() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
        }
        console.log('🧹 Interface limpa');
    }
}

// === FUNÇÕES GLOBAIS ===

// Compatibilidade com HTML
window.sendMessage = function() {
    if (window.chatInterface) {
        window.chatInterface.sendMessage();
    }
};

window.toggleTheme = function() {
    if (window.chatInterface) {
        window.chatInterface.toggleTheme();
    }
};

window.toggleCommands = function() {
    if (window.chatInterface) {
        window.chatInterface.toggleQuickCommands();
    }
};

window.toggleEmojis = function() {
    // Placeholder para futura implementação de emoji picker
    console.log('Emoji picker - em desenvolvimento');
};

window.insertCommand = function(command) {
    if (window.chatInterface) {
        window.chatInterface.insertCommand(command);
    }
};

window.exportChat = function() {
    if (window.chatInterface) {
        window.chatInterface.exportChatHistory();
    }
};

window.clearChat = function() {
    if (window.chatInterface) {
        window.chatInterface.clearChatHistory();
    }
};

// === FUNÇÕES BÁSICAS DE FALLBACK ===

// Função básica para abrir modal
function openSellerIdModal() {
    console.log('� openSellerIdModal básica chamada');
    const modal = document.getElementById('sellerIdModal');
    if (modal) {
        modal.style.display = 'flex';
        console.log('✅ Modal aberto');
        
        const input = document.getElementById('sellerIdInput');
        if (input) {
            setTimeout(() => {
                input.focus();
                input.select();
                console.log('✅ Input focado');
            }, 100);
        }
    } else {
        console.error('❌ Modal não encontrado');
        const sellerId = prompt('Digite seu Seller ID:');
        if (sellerId && sellerId.trim()) {
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.value = `identificar ${sellerId.trim()}`;
                const sendButton = document.getElementById('sendButton');
                if (sendButton) {
                    sendButton.click();
                }
            }
        }
    }
}

// Função básica para confirmar seller ID
function confirmSellerIdBasic() {
    console.log('✅ confirmSellerIdBasic chamada');
    const input = document.getElementById('sellerIdInput');
    const messageInput = document.getElementById('messageInput');
    
    if (!input) {
        console.error('❌ Input não encontrado');
        return;
    }
    
    const sellerId = input.value.trim();
    console.log('� Seller ID:', sellerId);
    
    if (sellerId && messageInput) {
        messageInput.value = `identificar ${sellerId}`;
        
        // Fechar modal
        const modal = document.getElementById('sellerIdModal');
        if (modal) {
            modal.style.display = 'none';
            input.value = '';
        }
        
        // Enviar mensagem
        const sendButton = document.getElementById('sendButton');
        if (sendButton) {
            sendButton.click();
            console.log('✅ Mensagem enviada');
        } else if (window.chatInterface && window.chatInterface.sendMessage) {
            window.chatInterface.sendMessage();
        }
        
        // FORÇA ADICIONAL - tentar múltiplas formas
        setTimeout(() => {
            if (messageInput.value.trim()) {
                console.log('🔄 Forçando envio adicional...');
                
                // Tentar via chatInterface primeiro
                if (window.chatInterface) {
                    console.log('📤 Força 1: chatInterface.sendMessage');
                    window.chatInterface.sendMessage();
                }
                
                // Simular Enter no input
                setTimeout(() => {
                    if (messageInput.value.trim()) {
                        console.log('📤 Força 2: Simular Enter');
                        const enterEvent = new KeyboardEvent('keydown', {
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            which: 13,
                            bubbles: true
                        });
                        messageInput.dispatchEvent(enterEvent);
                    }
                }, 100);
            }
        }, 200);
        
        // Esconder alert de identificação
        const alert = document.getElementById('identificationAlert');
        if (alert) {
            alert.classList.add('hidden');
        }
        localStorage.setItem('userIdentified', 'true');
    } else {
        alert('Por favor, digite seu seller_id');
        if (input) input.focus();
    }
}

// Função básica para fechar modal
function closeSellerIdModalBasic() {
    console.log('🔒 closeSellerIdModalBasic chamada');
    const modal = document.getElementById('sellerIdModal');
    const input = document.getElementById('sellerIdInput');
    
    if (modal) {
        modal.style.display = 'none';
        console.log('✅ Modal fechado');
    }
    
    if (input) {
        input.value = '';
        console.log('✅ Input limpo');
    }
}

// Função de DIAGNÓSTICO COMPLETO
window.diagnostico = function() {
    console.log('🏥 === DIAGNÓSTICO COMPLETO DO SISTEMA ===');
    
    // 1. Verificar elementos DOM
    console.log('📋 1. ELEMENTOS DOM:');
    const elementos = {
        messageInput: document.getElementById('messageInput'),
        sendButton: document.getElementById('sendButton'),
        chatMessages: document.getElementById('chatMessages'),
        sellerIdModal: document.getElementById('sellerIdModal'),
        sellerIdInput: document.getElementById('sellerIdInput')
    };
    
    Object.entries(elementos).forEach(([nome, elemento]) => {
        console.log(`  - ${nome}:`, !!elemento);
        if (elemento) {
            console.log(`    └─ Classes:`, elemento.className);
            if (elemento.style.display) {
                console.log(`    └─ Display:`, elemento.style.display);
            }
        }
    });
    
    // 2. Verificar funções globais
    console.log('🔧 2. FUNÇÕES GLOBAIS:');
    const funcoes = [
        'promptSellerId', 'confirmSellerId', 'closeSellerIdModal',
        'testModal', 'testIdentification', 'testSimple'
    ];
    
    funcoes.forEach(funcao => {
        console.log(`  - ${funcao}:`, typeof window[funcao]);
    });
    
    // 3. Verificar chatInterface
    console.log('🤖 3. CHAT INTERFACE:');
    if (window.chatInterface) {
        console.log('  - Instância existe:', true);
        console.log('  - Session ID:', window.chatInterface.sessionId);
        console.log('  - isLoading:', window.chatInterface.isLoading);
        console.log('  - sendMessage:', typeof window.chatInterface.sendMessage);
    } else {
        console.log('  - Instância existe:', false);
    }
    
    // 4. Teste de conectividade
    console.log('🌐 4. TESTE DE CONECTIVIDADE:');
    fetch('/api/status')
        .then(response => {
            console.log('  - Status API:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('  - Resposta:', data);
        })
        .catch(error => {
            console.error('  - Erro:', error);
        });
    
    console.log('🏥 === FIM DO DIAGNÓSTICO ===');
    
    return {
        elementos,
        chatInterface: window.chatInterface,
        funcoes: funcoes.map(f => ({ nome: f, tipo: typeof window[f] }))
    };
};

// === INICIALIZAÇÃO ===

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM carregado, iniciando sistema...');
    
    // Verificar elementos essenciais
    console.log('🔍 Verificando elementos DOM:');
    console.log('  - chatMessages:', !!document.getElementById('chatMessages'));
    console.log('  - messageInput:', !!document.getElementById('messageInput'));
    console.log('  - sendButton:', !!document.getElementById('sendButton'));
    console.log('  - sellerIdModal:', !!document.getElementById('sellerIdModal'));
    console.log('  - sellerIdInput:', !!document.getElementById('sellerIdInput'));
    
    // Configurar Enter no input do seller ID
    const sellerIdInput = document.getElementById('sellerIdInput');
    if (sellerIdInput) {
        sellerIdInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                console.log('⌨️ Enter pressionado no input do seller ID');
                window.confirmSellerId();
            }
        });
        console.log('✅ Listener Enter configurado para sellerIdInput');
    }
    
    // Configurar clique fora do modal para fechar
    const modal = document.getElementById('sellerIdModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                console.log('🖱️ Clique fora do modal detectado');
                window.closeSellerIdModal();
            }
        });
        console.log('✅ Listener clique fora configurado para modal');
    }
    
    // Inicializar interface profissional
    try {
        window.chatInterface = new ChatInterface();
        console.log('✅ ChatInterface inicializada com sucesso');
    } catch (error) {
        console.error('❌ Erro ao inicializar ChatInterface:', error);
    }
    
    // Verificar se deve exibir o alert de identificação
    window.checkIdentificationAlert();
    
    console.log('🚀 PC-Estoque Professional Chatbot Interface carregada');
    if (window.chatInterface) {
        console.log('Session ID:', window.chatInterface.sessionId);
    }
    
    // Teste do botão identificar
    console.log('🧪 Testando função promptSellerId...');
    if (typeof window.promptSellerId === 'function') {
        console.log('✅ window.promptSellerId está disponível');
        
        // Teste adicional - verificar se os elementos DOM estão disponíveis
        setTimeout(() => {
            console.log('🔍 Teste detalhado dos elementos:');
            const modal = document.getElementById('sellerIdModal');
            const input = document.getElementById('sellerIdInput');
            console.log('Modal DOM:', modal);
            console.log('Input DOM:', input);
            console.log('Modal display style:', modal ? modal.style.display : 'N/A');
        }, 1000);
    } else {
        console.error('❌ window.promptSellerId NÃO está disponível');
    }
    
    // Easter egg
    console.log('%c🤖 PC-Estoque Chatbot Professional', 
        'font-size: 20px; color: #667eea; font-weight: bold;');
    console.log('%cDesenvolvido com ❤️ para controle inteligente de estoque', 
        'font-size: 12px; color: #4a5568;');
});

// Exportar para módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatInterface;
}

// === FUNÇÕES GLOBAIS PARA AS NOVAS FUNCIONALIDADES ===

// Autocomplete
window.selectSuggestion = function(command) {
    if (window.chatInterface) {
        const input = window.chatInterface.inputElement;
        if (input) {
            input.value = command;
            window.chatInterface.updateCharacterCount();
            window.chatInterface.hideAutocomplete();
            input.focus();
        }
    }
};

// Notification Center
window.viewNotifications = function() {
    const center = document.getElementById('notificationCenter');
    if (center) {
        center.classList.add('open');
    }
};

window.closeNotificationCenter = function() {
    const center = document.getElementById('notificationCenter');
    if (center) {
        center.classList.remove('open');
    }
};

window.markAllAsRead = function() {
    if (window.chatInterface) {
        window.chatInterface.notifications.forEach(n => n.read = true);
        window.chatInterface.updateNotificationBadge();
    }
};

window.handleCriticalStock = function() {
    if (window.chatInterface) {
        window.chatInterface.inputElement.value = 'estoque-baixo';
        window.chatInterface.sendMessage();
        window.closeNotificationCenter();
    }
};

// Voice input
window.toggleVoiceInput = function() {
    if (window.chatInterface) {
        window.chatInterface.toggleVoiceInput();
    }
};

// Identificação Alert
window.hideIdentificationAlert = function() {
    const alert = document.getElementById('identificationAlert');
    if (alert) {
        alert.classList.add('hidden');
        // Salvar no localStorage que o usuário fechou o alert
        localStorage.setItem('identificationAlertHidden', 'true');
    }
};

// Verificar se o alert deve ser exibido ao carregar a página
window.checkIdentificationAlert = function() {
    const alert = document.getElementById('identificationAlert');
    const hidden = localStorage.getItem('identificationAlertHidden');
    const identified = localStorage.getItem('userIdentified');
    
    if (alert && (hidden === 'true' || identified === 'true')) {
        alert.classList.add('hidden');
    }
};

// Template insertion
window.insertQuickTemplate = function() {
    const templates = [
        'identificar seller123',
        'listar',
        'estoque-baixo',
        'config'
    ];
    
    const randomTemplate = templates[Math.floor(Math.random() * templates.length)];
    if (window.chatInterface) {
        window.chatInterface.inputElement.value = randomTemplate;
        window.chatInterface.inputElement.focus();
    }
};

// Função para inserir comando rápido clicado
window.insertQuickCommand = function(command) {
    if (window.chatInterface && window.chatInterface.inputElement) {
        window.chatInterface.inputElement.value = command;
        window.chatInterface.inputElement.focus();
        window.chatInterface.updateCharacterCount();
        
        // Scroll até o input
        window.chatInterface.inputElement.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }
};
