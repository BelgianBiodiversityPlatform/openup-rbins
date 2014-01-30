# Generate Magick::Image objects from text
#  * wraps text around width_constraint (pixels)
#  * cuts off text (and appends '...') if it goes beyond height_constraint (pixels)
#
# Example
# <code>
#    require 'rmagick_text_util.rb'
#    include RMagickTextUtil
#    some_text = "Hello world. This is a rather lengthy line "      +
#                "and I'm not very sure how much will be cropped, " +
#                "and how much will be left over. So, here goes!"
#
#    image = render_cropped_text(some_text, 100, 50)
#    image.write "example_without_block.jpg"
#
#    image = render_cropped_text(some_text, 100, 50) do |img|
#       img.fill = "#ff0000" # this won't work until RMagick v1.15.3
#       img.pointsize = 15
#    end
#    image.write "example_with_block.jpg"
# </code>
#

module RMagickTextUtil
    def render_cropped_text(caption_text, width_constraint, height_constraint, &block)
        image = render_text(caption_text, width_constraint, &block)
        if height_constraint < image.rows
            percent = height_constraint.to_f / image.rows.to_f
            end_index = (caption_text.size * percent).to_i  # takes a leap into cropping
            image = render_text(caption_text[0..end_index] + "...", width_constraint, &block)
            while height_constraint < image.rows && end_index > 0 # reduce in big chunks until within range
                end_index -= 80
                image = render_text(caption_text[0..end_index] + "...", width_constraint, &block)
            end
            while height_constraint > image.rows                  # lengthen in smaller steps until exceed
                end_index += 10
                image = render_text(caption_text[0..end_index] + "...", width_constraint, &block)
            end
            while height_constraint < image.rows && end_index > 0 # reduce in baby steps until fit
                end_index -= 1
                image = render_text(caption_text[0..end_index] + "...", width_constraint, &block)
            end
        end
        image
    end

    def render_text(caption_text, width_constraint, &block)
        Magick::Image.read("caption:#{caption_text.to_s}") {
            # this wraps the text to fixed width
            self.size = width_constraint
            # other optional settings
            block.call(self) if block_given?
        }.first
    end
end