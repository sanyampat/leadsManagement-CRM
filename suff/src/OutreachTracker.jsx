import React, { useState, useEffect, useMemo } from 'react';
import { 
  Search, Filter, Plus, Phone, Mail, Globe, MessageSquare, 
  Copy, Check, ExternalLink, Trash2, Edit2, X, Briefcase, 
  Award, AlertCircle, RefreshCw, Send
} from 'lucide-react';

// Default initial data matching the exact schema from crm_import.json
const INITIAL_LEADS = [
  {
    id: "e6e70eaa-9dd8-4bf2-9088-8dcbff841614",
    business_name: "Apple Borivali Now Open for Customers",
    contact_name: "Store Manager",
    email: "borivali@apple.com",
    phone: "+919876543210",
    website: "http://apple.com/in",
    service: "webdesign",
    signal: "grand_opening",
    score: 8,
    status: "new",
    source: "mumbai_openings_rss",
    scraped_at: "2026-07-27T18:35:59.322120+00:00",
    notes: "Source article: https://news.google.com/...[cite: 2]",
    contact_status: "ready"
  },
  {
    id: "4f98e750-13b4-4392-925e-09a3e13e79aa",
    business_name: "FOREVERMARK DIAMOND JEWELLERY",
    contact_name: null,
    email: null,
    phone: null,
    website: null,
    service: "webdesign",
    signal: "grand_opening",
    score: 8,
    status: "new",
    source: "mumbai_openings_rss",
    scraped_at: "2026-07-27T18:35:59.322120+00:00",
    notes: "Needs website redesign after grand opening launch.[cite: 2]",
    contact_status: "needs_manual_lookup"
  },
  {
    id: "96af751c-d961-46c7-9168-3d8a673da599",
    business_name: "Subko The Beloved Coffee Shop",
    contact_name: "Rahul Mehta",
    email: "hello@subko.coffee",
    phone: "+919123456789",
    website: "https://subko.coffee",
    service: "videoediting",
    signal: "fitness_gym_video_potential",
    score: 10,
    status: "contacted",
    source: "osm_established_fitness",
    scraped_at: "2026-07-27T18:35:59.322120+00:00",
    notes: "High potential for promotional reel editing.[cite: 1, 2]",
    contact_status: "ready"
  }
];

// Pipeline stages defined in project README
const PIPELINE_STAGES = [
  { key: 'new', label: 'New', color: 'bg-blue-500/10 text-blue-400 border-blue-500/20' },
  { key: 'contacted', label: 'Contacted', color: 'bg-amber-500/10 text-amber-400 border-amber-500/20' },
  { key: 'replied', label: 'Replied', color: 'bg-purple-500/10 text-purple-400 border-purple-500/20' },
  { key: 'interested', label: 'Interested', color: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' },
  { key: 'won', label: 'Won', color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' },
  { key: 'lost', label: 'Lost', color: 'bg-rose-500/10 text-rose-400 border-rose-500/20' }
];

// Outreach templates with dynamic placeholders
const TEMPLATES = {
  webdesign: {
    whatsapp: "Hi {name}, I noticed {business} recently launched or expanded! I specialize in modern, high-converting websites for growing brands in Mumbai. Would you be open to a quick 2-minute video mockup of what a revamped site could look like?",
    email_subject: "Digital Presence for {business}",
    email_body: "Hi {name},\n\nCongratulations on the recent updates with {business}!\n\nI was looking into your online presence and noticed a massive opportunity to upgrade your website to attract more high-ticket clients. I build fast, mobile-optimized sites tailored for established businesses.\n\nAre you free for a brief 5-minute call this week to discuss a redesign concept?\n\nBest regards,\n[Your Name]"
  },
  videoediting: {
    whatsapp: "Hey {name}! Love what {business} is doing. I'm a video editor specializing in high-retention Reels and cinematic promos for lifestyle and fitness brands. Could I send over a sample edit tailored for your Instagram page?",
    email_subject: "Engaging Video Content for {business}",
    email_body: "Hi {name},\n\nI've been following {business} and really love the energy of your brand.\n\nVideo is currently driving the highest ROI for customer acquisition in Mumbai, and I specialize in producing cinematic social media promos and ads that convert viewers into foot traffic.\n\nWould you be open to seeing a quick portfolio folder of relevant work I've done?\n\nBest,\n[Your Name]"
  }
};

export default function OutreachTracker() {
  // State management using LocalStorage persistence[cite: 9]
  const [leads, setLeads] = useState(() => {
    const saved = localStorage.getItem('outreach_crm_leads');
    return saved ? JSON.parse(saved) : INITIAL_LEADS;
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [serviceFilter, setServiceFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  
  // Modals state
  const [selectedLeadForMessage, setSelectedLeadForMessage] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [currentLead, setCurrentLead] = useState(null);
  const [copied, setCopied] = useState(false);

  // Sync to local storage whenever leads change[cite: 9]
  useEffect(() => {
    localStorage.setItem('outreach_crm_leads', JSON.stringify(leads));
  }, [leads]);

  // Filtered and searched leads[cite: 9]
  const filteredLeads = useMemo(() => {
    return leads.filter(lead => {
      const matchesSearch = 
        lead.business_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lead.contact_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        lead.notes?.toLowerCase().includes(searchQuery.toLowerCase());
        
      const matchesService = serviceFilter === 'all' || lead.service === serviceFilter;
      const matchesStatus = statusFilter === 'all' || lead.status === statusFilter;

      return matchesSearch && matchesService && matchesStatus;
    });
  }, [leads, searchQuery, serviceFilter, statusFilter]);

  // Pipeline stage counts
  const stageCounts = useMemo(() => {
    const counts = {};
    PIPELINE_STAGES.forEach(stage => counts[stage.key] = 0);
    leads.forEach(lead => {
      if (counts[lead.status] !== undefined) counts[lead.status]++;
    });
    return counts;
  }, [leads]);

  // Handle lead status updates[cite: 9]
  const updateLeadStatus = (id, newStatus) => {
    setLeads(leads.map(l => l.id === id ? { ...l, status: newStatus } : l));
  };

  // Delete lead[cite: 9]
  const deleteLead = (id) => {
    if (window.confirm("Remove this lead from your pipeline?")) {
      setLeads(leads.filter(l => l.id !== id));
    }
  };

  // Save new or edited lead[cite: 9]
  const handleSaveLead = (e) => {
    e.preventDefault();
    if (isEditing) {
      setLeads(leads.map(l => l.id === currentLead.id ? currentLead : l));
    } else {
      const newLead = {
        ...currentLead,
        id: crypto.randomUUID(),
        status: 'new',
        score: currentLead.score || 5,
        scraped_at: new Date().toISOString(),
        contact_status: (currentLead.phone || currentLead.email) ? 'ready' : 'needs_manual_lookup'
      };
      setLeads([newLead, ...leads]);
    }
    setCurrentLead(null);
    setIsEditing(false);
  };

  // Generate personalized template text[cite: 9]
  const generateMessage = (lead, type = 'whatsapp') => {
    const template = TEMPLATES[lead.service] || TEMPLATES.webdesign;
    const name = lead.contact_name || "there";
    const business = lead.business_name || "your business";
    
    if (type === 'whatsapp') {
      return template.whatsapp.replace("{name}", name).replace("{business}", business);
    } else if (type === 'email_subject') {
      return template.email_subject.replace("{business}", business);
    } else {
      return template.email_body.replace("{name}", name).replace("{business}", business);
    }
  };

  // Copy message text to clipboard[cite: 9]
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Import JSON handler to load exported leads directly[cite: 2, 9]
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const importedLeads = JSON.parse(event.target.result);
        if (Array.isArray(importedLeads)) {
          setLeads(importedLeads);
          alert(`Successfully imported ${importedLeads.length} leads!`);
        }
      } catch (err) {
        alert("Invalid JSON file format.");
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans pb-12">
      {/* Top Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-tr from-indigo-500 to-purple-500 p-2 rounded-xl text-white shadow-lg shadow-indigo-500/20">
              <Briefcase className="w-5 h-5" />
            </div>
            <h1 className="font-bold text-lg tracking-tight">Outreach<span className="text-indigo-400">CRM</span></h1>
          </div>
          
          <div className="flex items-center space-x-3">
            <label className="cursor-pointer bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg text-sm font-medium transition flex items-center space-x-2 border border-slate-700">
              <RefreshCw className="w-4 h-4" />
              <span>Import crm_import.json</span>
              <input type="file" accept=".json" onChange={handleFileUpload} className="hidden" />
            </label>
            <button 
              onClick={() => {
                setCurrentLead({ business_name: '', contact_name: '', email: '', phone: '', website: '', service: 'webdesign', notes: '', score: 5 });
                setIsEditing(false);
              }}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 shadow-lg shadow-indigo-600/20"
            >
              <Plus className="w-4 h-4" />
              <span>Add Lead</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 mt-6 space-y-6">
        
        {/* Sales Pipeline Bar[cite: 9] */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {PIPELINE_STAGES.map(stage => (
            <div 
              key={stage.key} 
              onClick={() => setStatusFilter(statusFilter === stage.key ? 'all' : stage.key)}
              className={`p-3 rounded-xl border bg-slate-900/60 transition cursor-pointer flex flex-col justify-between ${
                statusFilter === stage.key ? 'ring-2 ring-indigo-500 border-transparent' : 'border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{stage.label}</span>
              <div className="flex items-baseline justify-between mt-2">
                <span className="text-2xl font-bold text-white">{stageCounts[stage.key] || 0}</span>
                <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${stage.color}`}>
                  {stage.label}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Filters & Search Controls[cite: 9] */}
        <div className="flex flex-col md:flex-row gap-3 bg-slate-900 p-4 rounded-xl border border-slate-800 justify-between items-center">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input 
              type="text"
              placeholder="Search leads, names, notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center space-x-3 w-full md:w-auto overflow-x-auto">
            <div className="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-medium">
              <button 
                onClick={() => setServiceFilter('all')}
                className={`px-3 py-1.5 rounded-md transition ${serviceFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                All Services
              </button>
              <button 
                onClick={() => setServiceFilter('webdesign')}
                className={`px-3 py-1.5 rounded-md transition ${serviceFilter === 'webdesign' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Web Design
              </button>
              <button 
                onClick={() => setServiceFilter('videoediting')}
                className={`px-3 py-1.5 rounded-md transition ${serviceFilter === 'videoediting' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Video Editing
              </button>
            </div>

            {statusFilter !== 'all' && (
              <button 
                onClick={() => setStatusFilter('all')}
                className="text-xs bg-slate-800 text-slate-300 px-3 py-2 rounded-lg hover:bg-slate-700 flex items-center space-x-1"
              >
                <span>Clear Filter</span>
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Lead Grid[cite: 9] */}
        {filteredLeads.length === 0 ? (
          <div className="text-center py-16 bg-slate-900/30 rounded-2xl border border-slate-800/50">
            <AlertCircle className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-slate-300">No leads found</h3>
            <p className="text-sm text-slate-500 mt-1">Try adjusting your search criteria or add a new contact.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredLeads.map(lead => {
              const currentStage = PIPELINE_STAGES.find(s => s.key === lead.status) || PIPELINE_STAGES[0];
              
              return (
                <div key={lead.id} className="bg-slate-900 rounded-xl border border-slate-800 p-5 flex flex-col justify-between space-y-4 hover:border-slate-700 transition group">
                  <div className="space-y-3">
                    {/* Header: Score and Status */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="bg-indigo-500/10 text-indigo-400 text-xs font-semibold px-2 py-0.5 rounded border border-indigo-500/20 flex items-center space-x-1">
                          <Award className="w-3 h-3" />
                          <span>Score: {lead.score || 0}</span>
                        </span>
                        <span className="text-[11px] text-slate-500 uppercase tracking-wider font-semibold">
                          {lead.service}
                        </span>
                      </div>
                      
                      <select 
                        value={lead.status}
                        onChange={(e) => updateLeadStatus(lead.id, e.target.value)}
                        className={`text-xs font-medium px-2.5 py-1 rounded-full border cursor-pointer focus:outline-none ${currentStage.color} bg-slate-950`}
                      >
                        {PIPELINE_STAGES.map(s => (
                          <option key={s.key} value={s.key} className="bg-slate-900 text-slate-200">
                            {s.label}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Business Name & Contact */}
                    <div>
                      <h3 className="font-bold text-base text-white group-hover:text-indigo-400 transition line-clamp-1" title={lead.business_name}>
                        {lead.business_name}
                      </h3>
                      <p className="text-xs text-slate-400 mt-0.5">
                        {lead.contact_name ? `Contact: ${lead.contact_name}` : <span className="italic text-slate-600">No contact name</span>}
                      </p>
                    </div>

                    {/* Contact Links */}
                    <div className="flex items-center space-x-3 pt-1 text-xs text-slate-400">
                      {lead.phone && (
                        <a href={`tel:${lead.phone}`} className="flex items-center space-x-1 hover:text-emerald-400 transition">
                          <Phone className="w-3.5 h-3.5 text-slate-500" />
                          <span>{lead.phone}</span>
                        </a>
                      )}
                      {lead.email && (
                        <a href={`mailto:${lead.email}`} className="flex items-center space-x-1 hover:text-indigo-400 transition truncate max-w-[150px]">
                          <Mail className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                          <span className="truncate">{lead.email}</span>
                        </a>
                      )}
                      {lead.website && (
                        <a href={lead.website} target="_blank" rel="noreferrer" className="flex items-center space-x-1 hover:text-blue-400 transition ml-auto">
                          <Globe className="w-3.5 h-3.5 text-slate-500" />
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>

                    {/* Notes Snippet */}
                    {lead.notes && (
                      <p className="text-xs text-slate-500 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 line-clamp-2">
                        {lead.notes}
                      </p>
                    )}
                  </div>

                  {/* Actions Bar[cite: 9] */}
                  <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                    <button 
                      onClick={() => setSelectedLeadForMessage(lead)}
                      className="bg-indigo-600/10 hover:bg-indigo-600 text-indigo-400 hover:text-white border border-indigo-500/20 hover:border-transparent px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center space-x-1.5 w-full justify-center mr-2"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>Compose Outreach</span>
                    </button>
                    
                    <div className="flex items-center space-x-1">
                      <button 
                        onClick={() => { setCurrentLead(lead); setIsEditing(true); }}
                        className="p-1.5 text-slate-500 hover:text-slate-300 hover:bg-slate-800 rounded-md transition"
                        title="Edit Lead"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                      <button 
                        onClick={() => deleteLead(lead.id)}
                        className="p-1.5 text-slate-500 hover:text-rose-400 hover:bg-slate-800 rounded-md transition"
                        title="Delete Lead"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* Outreach Message Composer Modal[cite: 9] */}
      {selectedLeadForMessage && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="font-bold text-lg text-white">Outreach Composer</h3>
                <p className="text-xs text-slate-400">Targeting: <span className="text-indigo-400 font-semibold">{selectedLeadForMessage.business_name}</span></p>
              </div>
              <button onClick={() => setSelectedLeadForMessage(null)} className="text-slate-500 hover:text-white p-1">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* WhatsApp Section[cite: 9] */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase text-emerald-400 tracking-wider flex items-center space-x-1.5">
                  <MessageSquare className="w-3.5 h-3.5" />
                  <span>WhatsApp Template</span>
                </span>
                <button 
                  onClick={() => copyToClipboard(generateMessage(selectedLeadForMessage, 'whatsapp'))}
                  className="text-xs text-slate-400 hover:text-white flex items-center space-x-1"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? "Copied" : "Copy"}</span>
                </button>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 whitespace-pre-wrap font-mono">
                {generateMessage(selectedLeadForMessage, 'whatsapp')}
              </div>
              {selectedLeadForMessage.phone && (
                <a 
                  href={`https://wa.me/${selectedLeadForMessage.phone.replace(/[^0-9]/g, '')}?text=${encodeURIComponent(generateMessage(selectedLeadForMessage, 'whatsapp'))}`}
                  target="_blank" rel="noreferrer"
                  onClick={() => updateLeadStatus(selectedLeadForMessage.id, 'contacted')}
                  className="inline-flex items-center justify-center w-full bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-lg text-xs font-semibold transition shadow-lg shadow-emerald-600/20"
                >
                  Open in WhatsApp & Mark Contacted
                </a>
              )}
            </div>

            {/* Email Section[cite: 9] */}
            <div className="space-y-2 pt-2 border-t border-slate-800">
              <span className="text-xs font-semibold uppercase text-indigo-400 tracking-wider flex items-center space-x-1.5">
                <Mail className="w-3.5 h-3.5" />
                <span>Email Template</span>
              </span>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs text-slate-300 space-y-2 font-mono">
                <div className="border-b border-slate-800 pb-1 text-slate-400">
                  <span className="font-semibold text-slate-500">Subject:</span> {generateMessage(selectedLeadForMessage, 'email_subject')}
                </div>
                <div className="whitespace-pre-wrap">
                  {generateMessage(selectedLeadForMessage, 'email_body')}
                </div>
              </div>
              {selectedLeadForMessage.email && (
                <a 
                  href={`mailto:${selectedLeadForMessage.email}?subject=${encodeURIComponent(generateMessage(selectedLeadForMessage, 'email_subject'))}&body=${encodeURIComponent(generateMessage(selectedLeadForMessage, 'email_body'))}`}
                  onClick={() => updateLeadStatus(selectedLeadForMessage.id, 'contacted')}
                  className="inline-flex items-center justify-center w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 rounded-lg text-xs font-semibold transition shadow-lg shadow-indigo-600/20"
                >
                  Open Default Email & Mark Contacted
                </a>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Add/Edit Lead Modal[cite: 9] */}
      {currentLead && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <form onSubmit={handleSaveLead} className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-lg text-white">{isEditing ? "Edit Lead" : "Add New Lead"}</h3>
              <button type="button" onClick={() => { setCurrentLead(null); setIsEditing(false); }} className="text-slate-500 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-sm">
              <div>
                <label className="text-xs font-semibold text-slate-400">Business Name *</label>
                <input 
                  required type="text"
                  value={currentLead.business_name}
                  onChange={e => setCurrentLead({ ...currentLead, business_name: e.target.value })}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-400">Contact Person</label>
                  <input 
                    type="text"
                    value={currentLead.contact_name || ''}
                    onChange={e => setCurrentLead({ ...currentLead, contact_name: e.target.value })}
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-400">Service Category *</label>
                  <select 
                    value={currentLead.service}
                    onChange={e => setCurrentLead({ ...currentLead, service: e.target.value })}
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="webdesign">Web Design</option>
                    <option value="videoediting">Video Editing</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-400">Phone (+91...)</label>
                  <input 
                    type="text"
                    value={currentLead.phone || ''}
                    onChange={e => setCurrentLead({ ...currentLead, phone: e.target.value })}
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-400">Email</label>
                  <input 
                    type="email"
                    value={currentLead.email || ''}
                    onChange={e => setCurrentLead({ ...currentLead, email: e.target.value })}
                    className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400">Website URL</label>
                <input 
                  type="text"
                  value={currentLead.website || ''}
                  onChange={e => setCurrentLead({ ...currentLead, website: e.target.value })}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400">Notes / Signals</label>
                <textarea 
                  rows={2}
                  value={currentLead.notes || ''}
                  onChange={e => setCurrentLead({ ...currentLead, notes: e.target.value })}
                  className="w-full mt-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
              <button 
                type="button" 
                onClick={() => { setCurrentLead(null); setIsEditing(false); }}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-semibold transition"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition shadow-lg shadow-indigo-600/20"
              >
                {isEditing ? "Save Changes" : "Add Lead"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}