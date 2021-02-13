module Jekyll
  class SeoTag < Liquid::Tag

    def self.template_path
      @template_path ||= begin
        override = File.expand_path '../_includes/seo.html', File.dirname(__FILE__)
        override unless !File.exists? override
      end
    end
  end
end

Liquid::Template.register_tag('seo', Jekyll::SeoTag)
